# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 17:24:40 2019

@author: Caio Cid Santiago
"""

import os, sys
import json
import paho.mqtt.client as mqttc
from datetime import datetime
from imageai.Detection import ObjectDetection
from picamera import PiCamera

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

camera = PiCamera()

# Get the offset between local and UTC time
UTC_OFFSET = datetime.utcnow() - datetime.now()

now = datetime.now()
imgstamp = now.strftime("%d%m%Y-%H%M%S")

if not os.path.exists("safewatch_imgs/"):
    os.makedirs("safewatch_imgs/")
if not os.path.exists("safewatch_imgs/archive/"):
    os.makedirs("safewatch_imgs/archive/")
if not os.path.exists("safewatch_imgs/processed/"):
    os.makedirs("safewatch_imgs/processed/")

try:
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath( os.path.join(execution_path , "resnet.h5"))
    detector.loadModel(detection_speed="fast")

    # for r,d,f in os.walk(os.path.join(execution_path,"freeq_imgs","archive")):
    #     for file in f:
    #         now     = datetime.now()
    #         utc_now = now + UTC_OFFSET
    #         imgstamp = now.strftime("%d%m%Y-%H%M%S")
    #         imgpath    = os.path.join(execution_path, "freeq_imgs","archive",file)
    #         sourcepath = os.path.join(execution_path, "test","proc",file)
    
    #         detections = detector.detectObjectsFromImage(
    #             input_image=imgpath, output_image_path=sourcepath,
    #             minimum_percentage_probability=45)
    
    #         people = 0
    
    #         for eachObject in detections:
    #             if eachObject["name"] == "person":
    #                 people += 1
    #             print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
    
    #         print("\nPessoas identificadas: " + str(people))
    
    #         # Construct payload
    #         payload = {}
    #         payload["variable"] = "pessoas"
    #         payload["value"]    = people
    #         payload["unit"]     = now.strftime("às %H:%M (%d/%m/%Y)")
    #         payload["time"]     = utc_now.strftime("%Y-%m-%d %H:%M:%S")
    #         payload = json.dumps(payload)
    #         print("Payload: {}".format(payload))
    
    #         # Publish data
    #         client.publish(topic, payload=payload, qos=2)
    
    while True:
        now     = datetime.now()
        utc_now = now + UTC_OFFSET
        imgstamp = now.strftime("%d%m%Y-%H%M%S")
        imgpath    = execution_path + "/safewatch_imgs/archive/"   + imgstamp + ".jpg"
        sourcepath = execution_path + "/safewatch_imgs/processed/" + imgstamp + ".jpg"
        print("Capturando imagem... ", end="")
        camera.capture(os.path.join("", imgpath))
        print("Pronto!")

        detections = detector.detectObjectsFromImage(input_image=os.path.join('' , imgpath), output_image_path=os.path.join("", sourcepath))

        people = 0

        for eachObject in detections:
            if eachObject["name"] == "person":
                people += 1
            print(eachObject["name"] , " : " , eachObject["percentage_probability"] )

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
        
except KeyboardInterrupt:
    sys.exit()
