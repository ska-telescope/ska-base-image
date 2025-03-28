PROJECT=ska-base-image
CREATED=$(shell date -Iseconds)

include .make/base.mk
include .make/oci.mk
include .make/python.mk

PYTHON_LINT_TARGET = images/ska-webserver/resources
PYTHON_SWITCHES_FOR_PYLINT = \
	--max-locals 20

-include PrivateRules.mak

OCI_BUILD_ADDITIONAL_ARGS=--label int.skao.image.version="$(VERSION)" \
	--label int.skao.image.tags="$(TAG)" \
	--label int.skao.image.created="$(CREATED)"

oci-pre-build: ## Add metadata on the image
	rm -f $(OCI_IMAGE_ROOT_DIR)/$(strip $(OCI_IMAGE))/skao.metadata && \
	echo 'int.skao.image.created="$(CREATED)"' >> $(OCI_IMAGE_ROOT_DIR)/$(strip $(OCI_IMAGE))/skao.metadata && \
    echo 'int.skao.image.version="$(VERSION)"' >> $(OCI_IMAGE_ROOT_DIR)/$(strip $(OCI_IMAGE))/skao.metadata && \
    echo 'int.skao.image.tags="$(TAG)"' >> $(OCI_IMAGE_ROOT_DIR)/$(strip $(OCI_IMAGE))/skao.metadata && \
    echo 'int.skao.image.team="Systems Team"' >> $(OCI_IMAGE_ROOT_DIR)/$(strip $(OCI_IMAGE))/skao.metadata && \
    echo 'int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-image"' >> $(OCI_IMAGE_ROOT_DIR)/$(strip $(OCI_IMAGE))/skao.metadata && \
    echo 'int.skao.image.source="$(OCI_IMAGE_ROOT_DIR)/$(strip $(OCI_IMAGE))"' >> $(OCI_IMAGE_ROOT_DIR)/$(strip $(OCI_IMAGE))/skao.metadata && \
    echo 'int.skao.image.baseImage="${BASE_IMAGE}"' >> $(OCI_IMAGE_ROOT_DIR)/$(strip $(OCI_IMAGE))/skao.metadata
