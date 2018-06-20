FROM resin/rpi-raspbian
MAINTAINER Tobias Schoch <tobias.schoch@vtxmail.ch>


COPY requirements.txt /

# Install dependencies
RUN apt-get update && apt-get install libraspberrypi-bin python python-pip -y \
    --no-install-recommends && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt

COPY rpistatus /rpistatus
COPY mqtt.py /
COPY docker.py /
COPY main.py /

CMD ["python", "main.py"]