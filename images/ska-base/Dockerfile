FROM ubuntu:22.04

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-image" \
    int.skao.image.source="images/ska-base/Dockerfile" \
    int.skao.image.baseImage="ubuntu:22.04" 

USER root

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ca-certificates && \
    apt-get clean && \
    rm -fr /var/lib/apt/lists/*

COPY skao.metadata /etc/skao.metadata 

CMD ["bash"]
