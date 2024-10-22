ARG BASE_IMAGE="ska-base:0.1.1"
FROM $BASE_IMAGE

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-image" \
    int.skao.image.source="images/ska-build/Dockerfile"

ENV POETRY_VERSION=1.8.3

RUN apt-get update && apt-get install -y --no-install-recommends build-essential pipx libffi-dev python3-dev curl python-is-python3 python3-pip

RUN pipx install poetry==1.8.3
RUN pipx ensurepath

COPY skao.metadata /etc/skao.metadata

ENV PATH=$PATH:/root/.local/bin

CMD ["bash"]
