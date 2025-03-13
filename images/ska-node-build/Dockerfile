ARG BASE_IMAGE="ska-node:0.0.0"
FROM $BASE_IMAGE
ARG BASE_IMAGE_REF="ska-node:0.0.0"

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-node-build/Dockerfile" \
    int.skao.image.baseImage="${BASE_IMAGE_REF}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests build-essential git && \
    apt-get remove --purge --auto-remove -y && \
    rm -fr /var/lib/apt/lists/*

COPY skao.metadata /etc/skao.metadata

CMD ["bash"]
