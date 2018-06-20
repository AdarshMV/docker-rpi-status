Docker Raspberry Pi Status
===============================
author: Tobias Schoch

Overview
--------

Uses the vcgencmd tool from Broadcom to collect information about the current state of the Raspberry Pi and publishes on MQTT


Change-Log
----------
##### 0.0.2
* update readme
* working on rpi2 with services

##### 0.0.1
* initial version


Installation / Usage
--------------------
clone the repo:

```
git clone https://github.com/toschoch/docker-rpi-status.git
```
build the docker image
```
docker build . -t shocki/rpi-status
```

Example
-------

Run the container on a raspberry pi that publishes the vcgencmd data to a MQTT broker
```
docker run -d --rm --device /dev/vchiq -e MQTT_PW=... -e MQTT_SERVER=... -h=`hostname` --name rpi shocki/rpi-status
```

As devices in swarm deploys are not yet supported by docker. The `docker-compose.yml` cannot
yet be used.