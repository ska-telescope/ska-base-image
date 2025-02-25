ARG BASE_IMAGE="ska-node:0.0.0"
FROM $BASE_IMAGE
ARG BASE_IMAGE_REF="ska-node:0.0.0"

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-node-build/Dockerfile" \
    int.skao.image.baseImage="${BASE_IMAGE_REF}"

COPY skao.metadata /etc/skao.metadata

RUN apt update && \
    apt install -y --no-install-recommends build-essential git && \
    apt clean && \
    rm -fr /var/lib/apt/lists/*

CMD ["bash"]
