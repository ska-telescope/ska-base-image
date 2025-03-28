#!/usr/bin/env python3
"""
generate is used in docker-entrypoint.sh to dynamically generate an
nginx.conf pre-configured to serve static content and optionally
proxy calls to backends.
"""

import argparse
import ipaddress
import logging
import os
from pathlib import Path
from urllib.parse import urlparse

import yaml
from deepmerge import always_merger
from jinja2 import Template

LOGGING_FORMAT = (
    "%(asctime)s [level=%(levelname)s] "
    "[module=%(module)s] [line=%(lineno)d]: %(message)s"
)

logging.basicConfig(
    format=LOGGING_FORMAT,
    level=logging.INFO,
)

DEFAULT_INPUT_PATH = "/etc/nginx/templates/nginx.conf.j2"
DEFAULT_OUTPUT_PATH = "/etc/nginx/nginx.conf"
DEFAULT_CONFIG_PATH = "/etc/nginx/templates/config.yml"

DEFAULT_PROXY_CONFIG = {
    # Use HTTP/1.1 to support keep-alive and WebSocket upgrades if needed
    "proxy_http_version": "1.1",
    "proxy_set_header Host": "$host",
    "proxy_set_header X-Real-IP": "$remote_addr",
    "proxy_set_header X-Forwarded-For": "$remote_addr",
    "proxy_set_header X-Forwarded-Proto": "$scheme",
    "proxy_set_header X-Forwarded-Host": "$http_host",
    "proxy_set_header Proxy": '""',
    # Connection Upgrades (for WebSocket support)
    "proxy_set_header Upgrade": "$http_upgrade",
    "proxy_set_header Connection": '"upgrade"',
    # Data & Buffering
    "client_max_body_size": "1m",
    "proxy_connect_timeout": "10s",
    "proxy_read_timeout": "60s",
    "proxy_send_timeout": "60s",
    "proxy_buffering": "off",
    "proxy_buffers": "16 16k",
    "proxy_buffer_size": "32k",
    # Cookies
    "proxy_cookie_domain": "off",
    "proxy_cookie_path": "off",
    # Upstream management
    "proxy_next_upstream": "error timeout",
    "proxy_next_upstream_timeout": "0",
    "proxy_next_upstream_tries": "3",
    "proxy_redirect": "off",
}


def merge(a: dict, b: dict) -> dict:
    """
    merge does deep merging of two dictionaries
    """
    for key, value in b.items():
        if isinstance(value, dict):
            node = a.setdefault(key, {})
            merge(value, node)
        else:
            a[key] = value

    return a


def main(cliargs):
    """
    Generate nginx.conf dynamically given CLI parameters
    """
    logging.info("Generating %s", cliargs.output)
    with open(cliargs.input, "r", encoding="utf-8") as template_file:
        template_str = template_file.read()

    if not os.path.isdir(cliargs.config):
        raise ValueError(
            f"{cliargs.config} configuration directory doesn't exist or\
it is not readable",
        )

    config = {}
    for file in cliargs.config.glob("*.y*ml"):
        with open(file, "r", encoding="utf-8") as config_file:
            logging.info("Parsing configurations from '%s'", file)
            config = always_merger.merge(config, yaml.safe_load(config_file))

    config = always_merger.merge(
        config,
        {
            "env": {
                env_var["name"]: os.environ.get(
                    env_var["name"], env_var.get("default", None)
                )
                for env_var in config.get("config", {}).get("source_env", [])
            }
        },
    )

    # Treat the config as a template so that we can resolve self references
    rendered_config = yaml.safe_load(
        Template(yaml.safe_dump(config)).render(**config)
    )
    while config != rendered_config:
        rendered_config = config
        config = yaml.safe_load(
            Template(yaml.safe_dump(config)).render(**config)
        )

    sanitized_locations = []
    for loc in config.get("config", {}).get("locations", []):
        name = loc["location"]
        del loc["location"]
        proxy_pass = urlparse(loc["proxy_pass"])
        upstream_host = proxy_pass.netloc
        upstream_port = None
        if ":" in upstream_host:
            upstream_host, upstream_port = upstream_host.split(":")

        try:
            ipaddress.IPv4Address(upstream_host)
            upstream_host = None
        except ValueError:
            scheme = proxy_pass.scheme
            path = proxy_pass.path
            port = f":{upstream_port}" if upstream_port else ""
            loc["proxy_pass"] = f"{scheme}://$proxy_upstream_name{port}{path}"

        sanitized_locations.append(
            {
                "proxy_location": name,
                "proxy_upstream_host": upstream_host,
                "proxy_config": always_merger.merge(DEFAULT_PROXY_CONFIG, loc),
            }
        )

    config["config"]["locations"] = sanitized_locations

    with open(cliargs.output, "w", encoding="utf-8") as output_file:
        output_file.write(Template(template_str).render(**config))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ska-webserver nginx.conf generator"
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path(DEFAULT_INPUT_PATH),
        help=f"Path to the input template \
(default: {DEFAULT_INPUT_PATH})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(DEFAULT_OUTPUT_PATH),
        help=f"Path to the generated nginx config \
(default: {DEFAULT_OUTPUT_PATH})",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path(DEFAULT_CONFIG_PATH),
        help=f"Path to a configuration file \
(default: {DEFAULT_CONFIG_PATH})",
    )

    main(parser.parse_args())
