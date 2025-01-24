"""
This script manages the deprecation of base images in a Harbor repository.

Main functionality:
- Identifies artefacts older than 6 months.
- Copies them to a designated "deprecated" repository.
- Deletes them from the original repository.

Required Environment Variables:
- HARBOR_URL: Base URL for the Harbor API.
- HARBOR_SOURCE_PROJECT: The name of the project containing the images.
- HARBOR_DEPRECATION_PROJECT: The name of the project where images will be deprecated to.
- ROBOT_DEPRECATION_ACCOUNT_USERNAME: Username for authentication.
- ROBOT_DEPRECATION_ACCOUNT_SECRET: Token for authentication.
- DEPRECATION_CONFIG: A JSON-formatted string that defines the deprecation time span (in days) and
the list of base images to be deprecated.
"""

import logging
import os
import requests
import json
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

HARBOR_URL = os.getenv("HARBOR_URL")
SOURCE_PROJECT = os.getenv("HARBOR_SOURCE_PROJECT")
DEST_PROJECT = os.getenv("HARBOR_DEPRECATED_PROJECT")
ROBOT_DEPRECATION_ACCOUNT_USERNAME = os.getenv("ROBOT_DEPRECATION_ACCOUNT_USERNAME")
ROBOT_DEPRECATION_ACCOUNT_SECRET = os.getenv("ROBOT_DEPRECATION_ACCOUNT_SECRET")
CONFIG = os.getenv("DEPRECATION_CONFIG")
if CONFIG is None:
  config = {
    "timedelta_days": 180, # 6 months in days
    "images": ["ska-base", "ska-build", "ska-python", "ska-build-python"]
  }
else:
  config = json.loads(CONFIG)
DEPRECATION_PERIOD = datetime.now() - timedelta(config.get("timedelta_days"))
IMAGES = config.get("images")

def list_artefacts(username, password, repo):
    """List all artefacts in the deprecated repository.

    Args:
        username (str): Harbor username for authentication.
        password (str): Harbor password for authentication.
        repo (str): Repository name of artefacts to deprecated.

    Returns:
        list: A list of artefacts (dictionaries) from the repository.
    """
    logging.info(f"Listing artefacts in {SOURCE_PROJECT}/{repo}...")
    url = f"{HARBOR_URL}/api/v2.0/projects/{SOURCE_PROJECT}/repositories/{repo}/artifacts"
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to list artefacts: {response.text}")
        response.raise_for_status()

def copy_artefact(username, password, repo, digest):
    """Copy the artefact to the Deprecated project.

    Args:
        username (str): Harbor username for authentication.
        password (str): Harbor password for authentication.
        repo (str): Repository name of artefacts to deprecated.
        digest (str): Digest of the artefact to copy.

    Returns:
        bool: True if the copy was successful, False otherwise.
    """
    logging.info(f"Copying artefact {digest} to {DEST_PROJECT}/{repo}...")
    url = f"{HARBOR_URL}/api/v2.0/projects/{DEST_PROJECT}/repositories/{repo}/artifacts?from={SOURCE_PROJECT}/{repo}@{digest}"
    response = requests.post(url, auth=(username, password))
    if response.status_code == 201:
        logging.info(f"Successfully copied artefact {digest}.")
        return True
    else:
        logging.error(f"Failed to copy artefact {digest}: {response.text}")
        return False

def delete_artefact(username, password, repo, digest):
    """Delete artefact from the source repository.

    Args:
        username (str): Harbor username for authentication.
        password (str): Harbor password for authentication.
        repo (str): Repository name of artefacts to deprecated.
        digest (str): Digest of the artefact to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    logging.info(f"Deleting artefact {digest} from {SOURCE_PROJECT}/{repo}...")
    url = f"{HARBOR_URL}/api/v2.0/projects/{SOURCE_PROJECT}/repositories/{repo}/artifacts/{digest}"
    response = requests.delete(url, auth=(username, password))
    if response.status_code == 200:
        logging.info(f"Successfully deleted artefact {digest}.")
        return True
    else:
        logging.error(f"Failed to delete artefact {digest}: {response.text}")
        return False

def main():
    """Main function to manage deprecation of Harbor base images.

    - Lists all repositories defined in CONFIG var.
    - Processes each artefact older than 6 months:
        - Copies the artefact to the deprecated repository.
        - Deletes the artefact from the source repository.
    """
    try:
        username = ROBOT_DEPRECATION_ACCOUNT_USERNAME
        password = ROBOT_DEPRECATION_ACCOUNT_SECRET

        for image in IMAGES:
            artefacts = list_artefacts(username, password, image)
            if len(artefacts) <= 1:
                logging.info(f"Skipping repository {image} as it contains only one artefact and should not be removed.")
                continue
            for artefact in artefacts:
                digest = artefact["digest"]
                created_at = datetime.strptime(artefact["push_time"], "%Y-%m-%dT%H:%M:%S.%fZ")

                if created_at < DEPRECATION_PERIOD:
                    logging.info(
                        f"Processing artifact from image '{image}' with digest '{digest}', created at '{created_at}'..."
                    )
                    if copy_artefact(username, password, image, digest):
                        if delete_artefact(username, password, image, digest):
                            logging.info(f"Artefact {digest} successfully moved to {DEST_PROJECT}/{image}.")
                        else:
                            logging.warning(f"Failed to delete artefact {digest} after copying.")
                    else:
                        logging.warning(f"Skipping deletion of {digest} due to copy failure.")
                else:
                    logging.info(f"Skipping artefact {digest} as it is less than 6 months old.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
