# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 21:47:08 2019

@author: Cid Santiago
"""

from imageai.Detection import ObjectDetection
import os, time

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
#detector.setModelTypeAsTinyYOLOv3()
#detector.setModelTypeAsYOLOv3()

detector.setModelPath(os.path.join(execution_path, "resnet.h5"))
detector.loadModel(detection_speed="fast")
#detection_speed="faster"
#detection_speed="fastest"
#detection_speed="flash"


avg = []
custom_objects = detector.CustomObjects(person=True)

for r,d,f in os.walk(os.path.join(execution_path,"freeq_imgs")):
    for file in f:
        
        start_time = time.time()
        detections = detector.detectCustomObjectsFromImage(
            custom_objects=custom_objects,
            input_image=os.path.join(execution_path,"freeq_imgs","archive",file), 
            output_image_path=os.path.join(execution_path ,"test","proc",file),
            minimum_percentage_probability=45)

        final_time = time.time()-start_time
		
        avg.append(float(final_time))
        print("Tempo de execução: ",final_time)
        people = 0
        
        for eachObject in detections:
            if eachObject["name"] == "person":
                people += 1
            print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
        
        print("\nPessoas identificadas: " + str(people))
