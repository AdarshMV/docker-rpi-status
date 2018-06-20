#!/usr/bin/python
# -*- coding: UTF-8 -*-
# created: 20.06.2018
# author:  TOS

import logging
import time
import os
import json

from mqtt import MQTTClient, MQTTMock
from docker import get_secret
import rpistatus

app_name = 'RPI-Status'
logging_interval = 5 # seconds

mqtt_server = os.environ.get('MQTT_SERVER','mqtt')
mqtt_pw = get_secret('MQTT_PW')

topic = "devices/{hostname}/{subtopic}"

if __name__ == '__main__':

    log = logging.getLogger(app_name)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

    hostname = rpistatus.hostname()
    mqttc = MQTTClient(mqtt_server, client_id=hostname)
    mqttc._client.username_pw_set(app_name.lower(), mqtt_pw)

    status_topic = topic.format(hostname=hostname, subtopic='status')
    mqttc._client.will_set(status_topic, qos=1, payload=json.dumps({'status': 'stopped', 'ip': 'unknown'}), retain=True)

    data = {'ip': rpistatus.ipadress(), 'status': 'active'}
    mqttc.publish(topic=status_topic, payload=json.dumps(data), qos=1, retain=True)

    log.info("Start {} logging...".format(app_name))

    while True:
        t0 = time.time()

        for subtopic in ['camera','memory','clock','voltage','temperature','config']:
            data = getattr(rpistatus,subtopic)()
            data['time'] = time.time()
            log.info("publish to topic '{}': {}".format(topic.format(hostname=hostname, subtopic=subtopic),data))
            mqttc.publish(topic=topic.format(hostname=hostname, subtopic=subtopic),
                          payload=json.dumps(data), qos=1, retain=True)

        data = {'ip': rpistatus.ipadress(), 'status': 'active'}
        log.info("publish to topic '{}': {}".format(status_topic,data))
        mqttc.publish(topic=status_topic, payload=json.dumps(data), qos=1, retain=True)

        while (time.time()-t0)<logging_interval:
            time.sleep(0.1)

    log.info("Stop logging...")