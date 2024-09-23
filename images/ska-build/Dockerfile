FROM ska-base:0.1.0

ENV POETRY_VERSION=1.8.3

RUN RUN apt-get update && apt-get install -y --no-install-recommends build-essential pipx libffi-dev python-dev
RUN pipx ensurepath
RUN pipx install poetry==1.8.3

CMD ["bash"]
