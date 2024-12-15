from face_encoder import FaceEncoder
import face_recognition 
import time 
import torch
import threading
import numpy as np
import os
import cv2 
from facenet_pytorch import InceptionResnetV1
from ultralytics import YOLO


face_encoder1 = FaceEncoder()
model1=YOLO('yolov8n_100e.pt')
resnet = InceptionResnetV1(pretrained='vggface2').eval()
names = np.array([], dtype=object)
faces=[]


for image in os.listdir('faces'):
    face=cv2.imread(f"faces/{image}")
    result1=model1(face)  # use self.image instead of self.frame
    r1=result1[0]
    boxes1=r1.boxes
    if len(boxes1)>=1:
            bbox1=[int(i) for i in (boxes1[0]).xyxy[0]] 
            image0=face[bbox1[1]:bbox1[3],bbox1[0]:bbox1[2],:]
    face_encode=face_encoder1.encode_face(image0)
    faces.append(face_encode)
    print(len(faces))
    names=np.append(names,image.split('.')[0])

image5=cv2.imread("amber.jpg")
ebbed=face_encoder1.encode_face(image5)

result=face_encoder1.compare_faces(ebbed,faces)
print(result)