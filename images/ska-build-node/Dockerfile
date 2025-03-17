ARG BASE_IMAGE="ska-node:0.0.0"
FROM $BASE_IMAGE
ARG BASE_IMAGE_REF="ska-node:0.0.0"

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-build-node/Dockerfile" \
    int.skao.image.baseImage="${BASE_IMAGE_REF}"

# Select these versions based upon the version in cypress/browsers:<node version>
# export CYPRESS_BROWSERS_VERSION=22.14.0
# docker pull cypress/browsers:${CYPRESS_BROWSERS_VERSION};
# docker run --rm -it --entrypoint="npm" cypress/browsers:${CYPRESS_BROWSERS_VERSION} info cypress version
# > 14.2.0
# docker run --rm -it --entrypoint="google-chrome" cypress/browsers:${CYPRESS_BROWSERS_VERSION} --version
# > Google Chrome 134.0.6998.88

ENV CYPRESS_VERSION="14.2.0"
ENV CHROME_VERSION="134.0.6998.88"
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
    apt-get install --no-install-recommends --no-install-suggests -y build-essential git curl && \
    apt-get install --no-install-recommends --no-install-suggests -y xvfb libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libgtk-3-0 libgbm1 libasound2

RUN curl -fsSL http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb -o /usr/src/google-chrome-stable_current_amd64.deb && \
    apt-get install -f -y --no-install-recommends --no-install-suggests /usr/src/google-chrome-stable_current_amd64.deb && \
    rm -f /usr/src/google-chrome-stable_current_amd64.deb

RUN npm install --global "cypress@${CYPRESS_VERSION}" typescript && \
    apt-get remove --purge --auto-remove -y && \
    rm -rf /usr/share/doc && \
    rm -fr /var/lib/apt/lists/*

COPY skao.metadata /etc/skao.metadata

CMD ["bash"]
