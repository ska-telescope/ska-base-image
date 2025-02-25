ARG BASE_IMAGE="ska-base:0.0.0"
FROM $BASE_IMAGE
ARG BASE_IMAGE_REF="ska-base:0.0.0"

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-build/Dockerfile" \
    int.skao.image.baseImage="${BASE_IMAGE_REF}"

ENV POETRY_VERSION=1.8.3

RUN apt update && \
    apt install -y --no-install-recommends build-essential pipx libffi-dev python3-dev curl python-is-python3 python3-pip && \
    apt clean && \
    rm -fr /var/lib/apt/lists/*

RUN pipx install poetry==1.8.3
RUN pipx ensurepath

COPY skao.metadata /etc/skao.metadata

ENV PATH=$PATH:/root/.local/bin

CMD ["bash"]
