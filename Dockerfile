FROM ubuntu:22.04

USER root

RUN apt update && apt upgrade -y

CMD ["bash"]
