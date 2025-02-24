ARG BASE_IMAGE="ska-node:0.0.0"
FROM $BASE_IMAGE

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-node-build/Dockerfile" \
    int.skao.image.baseImage="$BASE_IMAGE"

COPY skao.metadata /etc/skao.metadata

CMD ["bash"]
