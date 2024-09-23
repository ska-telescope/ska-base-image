PROJECT=ska-base-image
CREATED=$(shell date -Iseconds)

# include OCI Images support
include .make/oci.mk

# include k8s support
include .make/k8s.mk

# include Helm Chart support
include .make/helm.mk

# Include Python support
include .make/python.mk

# include raw support
include .make/raw.mk

# include core make support
include .make/base.mk

# include your own private variables for custom deployment configuration
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
