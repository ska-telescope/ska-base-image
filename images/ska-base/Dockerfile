ARG BASE_IMAGE="ubuntu:22.04"
FROM $BASE_IMAGE

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-image" \
    int.skao.image.source="images/ska-base/Dockerfile" 

USER root

RUN apt-get update && apt-get upgrade -y

COPY skao.metadata /etc/skao.metadata 

CMD ["bash"]
