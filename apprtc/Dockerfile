FROM python:slim

RUN apt update && \
  apt upgrade -y && \
  apt install -y \
  libffi-dev \
  libssl-dev \
  build-essential \
  pkg-config \
  libvpx-dev \
  libopus-dev \
  libavfilter-dev \
  libavdevice-dev \
  libsrtp2-dev

WORKDIR /src/app
COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3"]
CMD ["/src/app/apprtc.py"]
