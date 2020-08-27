# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 17:24:40 2019

@author: Caio Cid Santiago
"""

import os, sys, time, json, random, serial
import paho.mqtt.client as mqttc
from datetime import datetime

# MQTT connect callback function
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker com sucesso!")
    else:
        print("Falha na conexão com broker. Código retornado: " + str(rc))

# MQTT publish callback function
def on_publish(client, userdata, mid):
    print("Mensagem " + str(mid) + " publicada...")

execution_path = os.getcwd()

# Broker configuration
broker_url  = "mqtt.tago.io"
broker_port = 8883
topic       = "safewatch/node1"
dev_token   = open("dev_token").read()[0:-1]

client = mqttc.Client()          # Instantiate client
client.on_connect = on_connect   # Bind 'on_connect' callback function
client.on_publish = on_publish   # Bind 'on_publish' callback function

client.username_pw_set("", dev_token)
client.tls_set()
client.connect(broker_url, broker_port)
client.loop_start()

# Get the offset between local and UTC time
UTC_OFFSET = datetime.utcnow() - datetime.now()

now = datetime.now()

ser = serial.Serial('COM3', 115200)
ser.flush()

try:  
    while True:
        now     = datetime.now()
        utc_now = now + UTC_OFFSET
        imgstamp = now.strftime("%d%m%Y-%H%M%S")
        
        line = ser.read_until().decode('utf-8').rstrip()
        print(line)
        if len(line.split('$')) > 2:
            test = line.split('$')
            print(test[1])
            package = json.loads(test[1])
            print(package)
            people = package['value']  


        print("\nPessoas identificadas: " + str(people))

        # Construct payload
        payload = {}
        payload["variable"] = "pessoas"
        payload["value"]    = people
        payload["unit"]     = now.strftime("às %H:%M (%d/%m/%Y)")
        payload["time"]     = utc_now.strftime("%Y-%m-%d %H:%M:%S")
        payload = json.dumps(payload)
        print("Payload: {}".format(payload))

        # Publish data
        client.publish(topic, payload=payload, qos=1)

        time.sleep(30)
        
except KeyboardInterrupt:
    sys.exit()
