ARG BASE_IMAGE="ska-base:0.1.1"
ARG VERSION
ARG TAG
ARG CREATED
FROM $BASE_IMAGE

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-python/Dockerfile"

COPY skao.metadata /etc/skao.metadata

RUN apt-get update && \
    apt-get install -y python3 python-is-python3 && \
    apt-get clean && \
    rm -fr /var/lib/apt/lists/*

CMD ["bash"]
