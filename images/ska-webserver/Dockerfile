ARG BASE_IMAGE="ska-node:0.0.0"
FROM $BASE_IMAGE
ARG BASE_IMAGE_REF="ska-node:0.0.0"

ENV NGINX_VERSION="1.27.3"

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-nginx/Dockerfile" \
    int.skao.image.baseImage="${BASE_IMAGE_REF}"

# https://github.com/nginxinc/docker-nginx/blob/master/mainline/debian/Dockerfile
# https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/#installing-prebuilt-ubuntu-packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests curl lsb-release && \
    curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor | tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/mainline/ubuntu `lsb_release -cs` nginx" | tee /etc/apt/sources.list.d/nginx.list && \
    echo "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" | tee /etc/apt/preferences.d/99nginx && \
    apt-get update && \
    groupadd --system --gid 101 nginx && \
    useradd --system --gid nginx --no-create-home --home /nonexistent --comment "nginx user" --shell /bin/false --uid 101 nginx && \
    apt-get install -y --no-install-recommends --no-install-suggests gettext-base nginx=${NGINX_VERSION}-1~jammy && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log && \
    apt-get remove --purge --auto-remove -y lsb-release && \
    rm -fr /var/lib/apt/lists/*

COPY resources/docker-entrypoint.sh /

# Pull from nginx official sources the default entrypoint scripts. Users can add more, mounting them to /docker-entrypoint.d/
RUN mkdir /docker-entrypoint.d && \
    ENTRYPOINTS="10-listen-on-ipv6-by-default.sh 15-local-resolvers.envsh 20-envsubst-on-templates.sh 30-tune-worker-processes.sh" && \
    for ENTRYPOINT in $ENTRYPOINTS; do curl -fsSL https://raw.githubusercontent.com/nginxinc/docker-nginx/refs/tags/${NGINX_VERSION}/mainline/debian/$ENTRYPOINT -o /docker-entrypoint.d/$ENTRYPOINT; done && \
    chmod +x docker-entrypoint.sh && \
    chmod +x -R /docker-entrypoint.d && \
    apt-get remove --purge --auto-remove -y curl && \
    rm -fr /var/lib/apt/lists/* && \
    rm -rf /usr/share/nginx/html/* && \
    rm -rf /etc/nginx/conf.d/*

COPY resources/nginx.conf.tpl /etc/nginx/templates/nginx.conf.tpl
COPY resources/favicon.ico /usr/share/nginx/html/favicon.ico

COPY skao.metadata /etc/skao.metadata

# Environment variables used to generate /etc/nginx/nginx.conf
ENV NGINX_WORKER_PROCESSES="auto"
ENV NGINX_WORKER_CONNECTIONS="1024"
ENV NGINX_LOG_LEVEL="warn"
ENV NGINX_PORT="80"
ENV NGINX_SERVER_NAME="_"
ENV NGINX_STATIC_FILE_CACHE_EXPIRATION="7d"
ENV NGINX_ROOT="/usr/share/nginx/html"

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE ${NGINX_PORT}

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]
