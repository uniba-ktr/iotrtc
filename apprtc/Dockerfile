FROM debian:buster-slim

RUN apt update && \
  apt upgrade -y && \
  apt install -y \
  python3 \
  python3-pip \
  python3-dev \
  libffi-dev \
  libssl-dev \
  build-essential \
  pkg-config \
  libvpx-dev \
  libopus-dev \
  libavfilter-dev \
  libavdevice-dev \
  libsrtp2-dev

RUN pip3 install setuptools && \
  pip3 install \
  asyncio \
  aiohttp \
  websockets \
  attrs \
  av \
  cffi \
  crc32c \
  cryptography \
  pyee \
  pylibsrtp \
  pyopenssl \
  netifaces \
  asn1crypto \
  six \
  aioice

RUN pip3 install requests

WORKDIR /src/app

COPY . .

ENTRYPOINT ["python3"] 
CMD ["/src/app/apprtc.py"]
