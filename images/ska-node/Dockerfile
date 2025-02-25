ARG BASE_IMAGE="ska-base:0.0.0"
FROM $BASE_IMAGE
ARG BASE_IMAGE_REF="ska-base:0.0.0"

ARG NODE_RELEASE="22"
ARG NPM_VERSION="10.9.0"
ARG YARN_VERSION="1.22.22"

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-node/Dockerfile" \
    int.skao.image.baseImage="${BASE_IMAGE_REF}"

COPY skao.metadata /etc/skao.metadata

RUN apt update && \
    apt install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_${NODE_RELEASE}.x -o nodesource.sh && \
    bash -C nodesource.sh  && \
    rm nodesource.sh && \
    apt install -y nodejs && \
    npm install --global npm@${NPM_VERSION} yarn@${YARN_VERSION} && \ 
    apt purge -y --auto-remove curl && \
    apt clean && \
    rm -fr /var/lib/apt/lists/*

CMD ["bash"]
