import requests
from datetime import datetime, timedelta
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

HARBOR_URL = os.getenv("HARBOR_URL")
PROJECT = os.getenv("HARBOR_DEPRECATION_PROJECT")
DEST_REPO = os.getenv("HARBOR_DEPRECATION_REPO")
ROBOT_DEPRECATION_ACCOUNT_USERNAME = os.getenv("ROBOT_DEPRECATION_ACCOUNT_USERNAME")
ROBOT_DEPRECATION_ACCOUNT_SECRET = os.getenv("ROBOT_DEPRECATION_ACCOUNT_SECRET")

# Time threshold for deprecation
SIX_MONTHS_AGO = datetime.now() - timedelta(days=180)

# List artifacts in the source repository
def list_artifacts(username, password, repo):
    logging.info(f"Listing artifacts in {PROJECT}/{repo}...")
    url = f"{HARBOR_URL}/api/v2.0/projects/{PROJECT}/repositories/{repo}/artifacts"
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Failed to list artifacts: {response.text}")
        response.raise_for_status()

# Copy artifact to the deprecated repository
def copy_artifact(username, password, repo, digest):
    logging.info(f"Copying artifact {digest} to {PROJECT}/{DEST_REPO}...")
    url = f"{HARBOR_URL}/api/v2.0/projects/{PROJECT}/repositories/{DEST_REPO}/artifacts?from={PROJECT}/{repo}@{digest}"
    response = requests.post(url, auth=(username, password))
    if response.status_code == 201:
        logging.info(f"Successfully copied artifact {digest}.")
        return True
    else:
        logging.error(f"Failed to copy artifact {digest}: {response.text}")
        return False

# Add new tag to artifact and remove old tag
def add_new_tag(username, password, repo, digest, artifact):
    # Update the "name" key in each tag dictionary
    tags = artifact.get("tags", [])
    for tag in tags:
        old_tag_name = tag["name"]
        new_tag_name = f"{repo}-{tag['name']}"

         # Update the "name" field in the tag dictionary
        tag["name"] = new_tag_name        
        
        # Add new tag
        logging.info(f"Adding new tag '{new_tag_name}':\n {tag}\n to artifact {digest}...")
        add_url = f"{HARBOR_URL}/api/v2.0/projects/{PROJECT}/repositories/{DEST_REPO}/artifacts/{digest}/tags/"
        payload = tag
        response = requests.post(add_url, json=payload, auth=(username, password))
        if response.status_code == 201:
            logging.info(f"Successfully added new tag '{new_tag_name}' to artifact {digest}.")
        else:
            logging.error(f"Failed to add new tag '{new_tag_name}' to artifact {digest}: {response.text}")
            return False

        # Remove old tag
        logging.info(f"Removing old tag '{old_tag_name}' from artifact {digest}...")
        delete_url = f"{HARBOR_URL}/api/v2.0/projects/{PROJECT}/repositories/{DEST_REPO}/artifacts/{digest}/tags/{old_tag_name}"
        response = requests.delete(delete_url, auth=(username, password))
        if response.status_code == 200:
            logging.info(f"Successfully deleted old tag '{old_tag_name}' from artifact {digest}.")
        else:
            logging.error(f"Failed to delete old tag '{old_tag_name}' from artifact {digest}: {response.text}")
            return False
    return True

def delete_artifact(username, password, repo, digest):
    logging.info(f"Deleting artifact {digest} from {PROJECT}/{repo}...")
    url = f"{HARBOR_URL}/api/v2.0/projects/{PROJECT}/repositories/{repo}/artifacts/{digest}"
    response = requests.delete(url, auth=(username, password))
    if response.status_code == 200:
        logging.info(f"Successfully deleted artifact {digest}.")
        return True
    else:
        logging.error(f"Failed to delete artifact {digest}: {response.text}")
        return False

def main():
    try:
        username = ROBOT_DEPRECATION_ACCOUNT_USERNAME
        password = ROBOT_DEPRECATION_ACCOUNT_SECRET

        # Fetch ska-base-images
        script_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(script_dir, os.pardir, "images")
        images_dir = os.path.abspath(images_dir)
        images = [f for f in os.listdir(images_dir) if os.path.isdir(os.path.join(images_dir, f))]
        logging.info(f"Base image name: {images}")

        for image in images:
            artifacts = list_artifacts(username, password, image)
            if len(artifacts) <= 1:
                logging.info(f"Skipping repository {image} as it contains only one artifact.")
                continue
            for artifact in artifacts:
                digest = artifact["digest"]
                created_at = datetime.strptime(artifact["push_time"], "%Y-%m-%dT%H:%M:%S.%fZ")

                if created_at < SIX_MONTHS_AGO:
                    logging.info(f"Processing artifact {digest}, created at {created_at}...")

                    if copy_artifact(username, password, image, digest):
                        add_new_tag(username, password, image, digest, artifact)
                        if delete_artifact(username, password, image, digest):
                            logging.info(f"Artifact {digest} successfully moved to {PROJECT}/{DEST_REPO}.")
                        else:
                            logging.warning(f"Failed to delete artifact {digest} after copying.")
                    else:
                        logging.warning(f"Skipping deletion of {digest} due to copy failure.")
                else:
                    logging.info(f"Skipping artifact {digest} as it is less than 6 months old.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
