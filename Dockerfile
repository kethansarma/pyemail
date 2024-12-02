FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    thunderbird \
    dbus-x11 \
    x11-utils \
    xvfb \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY send_email.py /root/send_email.py

WORKDIR /root

CMD ["xvfb-run", "--auto-servernum", "--server-args='-screen 0 1024x768x24'", "python3", "send_email.py"]
