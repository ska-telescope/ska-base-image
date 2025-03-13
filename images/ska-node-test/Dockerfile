ARG BASE_IMAGE="ska-node:0.0.0"
FROM $BASE_IMAGE
ARG BASE_IMAGE_REF="ska-node:0.0.0"

# Select these versions based upon the version in cypress/browsers:<node version>
# docker run --rm -it --entrypoint=/bin/sh cypress/browsers:22.14.0
# $ google-chrome --version
# > Google Chrome 133.0.6943.53
# $ npm info cypress version
# > 14.0.3
ENV CYPRESS_VERSION="14.0.3"
ENV CHROME_VERSION="133.0.6943.53"

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-node-test/Dockerfile" \
    int.skao.image.baseImage="${BASE_IMAGE_REF}"

# https://github.com/cypress-io/cypress-docker-images/blob/master/factory/factory.Dockerfile"
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null \
    TERM=xterm \
    npm_config_loglevel=warn \
    CI=1 \
    QT_X11_NO_MITSHM=1 \
    _X11_NO_MITSHM=1 \
    _MITSHM=0 \
    CYPRESS_CACHE_FOLDER=/root/.cache/Cypress

# https://github.com/cypress-io/cypress-docker-images/blob/master/factory/installScripts
RUN apt-get update && \
    mkdir -p ${CYPRESS_CACHE_FOLDER} && \
    chmod 777 -R /root /root/.cache && \
    apt-get install --no-install-recommends --no-install-suggests -y curl xvfb libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libgtk-3-0 libgbm1 libasound2

RUN curl -fsSL http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb -o /usr/src/google-chrome-stable_current_amd64.deb && \
    apt-get install -f -y --no-install-recommends --no-install-suggests /usr/src/google-chrome-stable_current_amd64.deb && \
    rm -f /usr/src/google-chrome-stable_current_amd64.deb

RUN npm install --global "cypress@${CYPRESS_VERSION}" typescript && \
    apt-get remove --purge --auto-remove -y curl && \
    rm -rf /usr/share/doc && \
    rm -fr /var/lib/apt/lists/*

COPY skao.metadata /etc/skao.metadata

CMD ["bash"]
