FROM ubuntu:22.04

LABEL int.skao.image.team="Systems Team" \
    int.skao.image.url="https://gitlab.com/ska-telescope/ska-base-images" \
    int.skao.image.source="images/ska-base/Dockerfile" \
    int.skao.image.baseImage="ubuntu:22.04"

USER root

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends --no-install-suggests ca-certificates && \
    apt-get remove --purge --auto-remove -y && \
    rm -fr /var/lib/apt/lists/*

# CIS Level 2 / STIG remediations
RUN echo "Unattended-Upgrade::Remove-Unused-Dependencies \"true\";" >> /etc/apt/apt.conf.d/50unattended-upgrades && \
    echo "Unattended-Upgrade::Remove-Unused-Kernel-Packages \"true\";" >> /etc/apt/apt.conf.d/50unattended-upgrades && \
    find /var/log/ -perm /u+xs,g+xws,o+xwrt ! -name 'history.log' ! -name 'eipp.log.xz' ! -name '*[bw]tmp' ! -name '*lastlog' -type f -regextype posix-extended -regex '.*' -exec chmod u-xs,g-xws,o-xwrt {} \; && \
    sed -i "/^[^#]*\<maxlogins\>/ s/maxlogins.*/maxlogins 10/" /etc/security/limits.conf && \
    sed -ri 's/^.*hard\s+core\s+[[:digit:]]+/*     hard   core    0/' /etc/security/limits.conf && \
    echo "umask 027" >> /etc/bash.bashrc && \
    echo "umask 027" >> /etc/profile && \
    sed -ri 's/UMASK(\s+)[0-9]+/UMASK\1027/' /etc/login.defs

COPY skao.metadata /etc/skao.metadata 

CMD ["bash"]
