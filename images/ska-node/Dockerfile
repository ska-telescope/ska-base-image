ARG BASE_IMAGE="ska-base:0.0.0"
FROM $BASE_IMAGE
ARG BASE_IMAGE_REF="ska-base:0.0.0"

ENV NODE_RELEASE="22"
ENV NPM_VERSION="10.9.0"
ENV YARN_VERSION="1.22.22"

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-node/Dockerfile" \
    int.skao.image.baseImage="${BASE_IMAGE_REF}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests curl && \
    curl -fsSL https://deb.nodesource.com/setup_${NODE_RELEASE}.x -o nodesource.sh && \
    bash -C nodesource.sh  && \
    rm nodesource.sh && \
    apt-get install -y --no-install-recommends --no-install-suggests nodejs && \
    npm install --global npm@${NPM_VERSION} yarn@${YARN_VERSION} && \ 
    apt-get remove --purge --auto-remove -y curl && \
    rm -fr /var/lib/apt/lists/*

COPY skao.metadata /etc/skao.metadata

CMD ["bash"]
