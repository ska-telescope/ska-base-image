ARG BASE_IMAGE="ska-python:0.0.0"
FROM $BASE_IMAGE
ARG BASE_IMAGE_REF="ska-python:0.0.0"

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-build-python/Dockerfile" \
    int.skao.image.baseImage="${BASE_IMAGE_REF}"

ENV POETRY_VERSION=1.8.3

RUN apt-get update && \
    apt-get install -y --no-install-recommends --no-install-suggests build-essential git curl && \
    apt-get install -y --no-install-recommends --no-install-suggests pipx libffi-dev python3-pip && \
    apt-get remove --purge --auto-remove -y && \
    rm -fr /var/lib/apt/lists/*

RUN pipx install poetry==${POETRY_VERSION} && \
    pipx ensurepath

COPY skao.metadata /etc/skao.metadata

ENV PATH=$PATH:/root/.local/bin

CMD ["bash"]
