ARG BASE_IMAGE="ska-node:0.0.0"
FROM $BASE_IMAGE

# Select these versions based upon the version in cypress/browsers:<node version>
# docker run --rm -it --entrypoint=/bin/sh cypress/browsers:22.14.0
# $ google-chrome --version
# $ npm info cypress version
ARG CYPRESS_VERSION="14.0.3"
ARG CHROME_VERSION="133.0.6943.53"

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-node-test/Dockerfile" \
    int.skao.image.baseImage="$BASE_IMAGE"

# https://github.com/cypress-io/cypress-docker-images/blob/master/factory/factory.Dockerfile"
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null \
    TERM=xterm \
    npm_config_loglevel=warn \
    CI=1 \
    QT_X11_NO_MITSHM=1 \
    _X11_NO_MITSHM=1 \
    _MITSHM=0 \
    CYPRESS_CACHE_FOLDER=/root/.cache/Cypress

COPY skao.metadata /etc/skao.metadata

# https://github.com/cypress-io/cypress-docker-images/blob/master/factory/installScripts
RUN apt update && \
    mkdir -p ${CYPRESS_CACHE_FOLDER} && \
    chmod 777 -R /root /root/.cache && \
    apt install --no-install-recommends -y curl xvfb libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libgtk-3-0 libgbm1 libasound2 && \
    curl -fsSL http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb -o /usr/src/google-chrome-stable_current_amd64.deb && \
    apt install -f -y /usr/src/google-chrome-stable_current_amd64.deb && \
    rm -f /usr/src/google-chrome-stable_current_amd64.deb && \
    npm install --global "cypress@${CYPRESS_VERSION}" typescript \
    apt-get purge -y --auto-remove curl && \
    apt clean && \
    rm -rf /usr/share/doc && \
    rm -fr /var/lib/apt/lists/*

CMD ["bash"]
