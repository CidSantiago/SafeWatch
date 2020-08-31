import os, sys, serial
import json
from datetime import datetime
from imageai.Detection import ObjectDetection
from picamera import PiCamera

execution_path = os.getcwd()

camera = PiCamera()

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.flush()

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
        ser.write(str(people).encode())
        print("Enviado ao ESP!")
        
except KeyboardInterrupt:
    sys.exit()
