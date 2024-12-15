import face_recognition 
import time 
import threading
import numpy as np
import os
import cv2 
import paho.mqtt.client as mqtt
from facenet_pytorch import InceptionResnetV1
from ultralytics import YOLO
names = np.array([], dtype=object)
faces=[]
client=mqtt.Client(client_id="587364535763")

for image in os.listdir('faces'):
      face=cv2.imread(f"faces/{image}")
      encodings=face_recognition.face_encodings(face)[0]

      faces.append(encodings)
      print(len(faces))
      names=np.append(names,image.split('.')[0])
model1=YOLO('yolov8n_100e.pt')

class Process:
        def __init__(self) :
            self.access=False
            self.frame=None 
            self.rec=None
            self.name='checking'
            self.bbox=None
            self.prev_name=None
            self.name_check=None
            self.image=None
            self.finish=True
            t1=threading.Thread(target=self.process_all_time)
            t2=threading.Thread(target=self.process_frames)
            t1.start()
            t2.start()

        def process_frames(self):
            while self.finish :
               if self.rec  :
                        time.sleep(3)
                        print('helo')
                        self.frame=cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
                        
                        locations=face_recognition.face_locations(self.frame)
                       

                        encoding=face_recognition.face_encodings(self.frame,locations)             
                        if len(encoding)>0 and len(encoding) < 2 :
                           
                            comparition=face_recognition.compare_faces(faces,encoding[0])
                            self.name_check=names[comparition]
                            
                            
                            if len(self.name_check)==0:
                                self.name='cheking'
                                self.prev_name=self.name
                                
                                 
                            elif len(self.name_check)==1:
                                 
                                 if self.prev_name != self.name_check[0]:
                                       self.prev_name=self.name_check[0]
                                       self.publish()

                                 self.name= self.name_check[0]
                                                     
        def publish(self):
                        client.connect('127.0.0.1', 1883)
                        client.publish("artifitial","access")
                        time.sleep(0.5)
                        client.disconnect()                   
        def process_all_time(self):
            video=cv2.VideoCapture(0)
            while True :
                self.rec,self.image=video.read()
                if self.rec :
                    result=model1(self.image)  # use self.image instead of self.frame
                    r=result[0]
                    boxes=r.boxes
                    if len(boxes)==1:
                        self.bbox=[int(i) for i in (boxes[0]).xyxy[0]]  
                         
                        cv2.putText(self.image, self.name, (self.bbox[0], self.bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)  
                        top_left = (self.bbox[0], self.bbox[1])
                        top_right = (self.bbox[2], self.bbox[1])
                        bottom_left = (self.bbox[0], self.bbox[3])
                        bottom_right = (self.bbox[2], self.bbox[3])

                        # Define the color and thickness of the lines
                        color = (255, 255, 0)  # yellow in BGR color space
                        thickness = 2
                        var=15
                        # Draw the four lines (edges of the rectangle)
                        cv2.line(self.image, top_left, (self.bbox[0], self.bbox[1]+var), color, thickness)
                        cv2.line(self.image, top_left, (self.bbox[0]+var, self.bbox[1]), color, thickness)
                        cv2.line(self.image,(self.bbox[2]-var, self.bbox[3]) , bottom_right, color, thickness)
                        cv2.line(self.image,(self.bbox[2], self.bbox[3]-var) , bottom_right , color, thickness)     
                        cv2.line(self.image,(self.bbox[0], self.bbox[3]-var) ,bottom_left , color, thickness)
                        cv2.line(self.image,bottom_left ,(self.bbox[0]+var, self.bbox[3]),  color, thickness)
                        cv2.line(self.image,top_right ,(self.bbox[2], self.bbox[1]+var) , color, thickness)
                        cv2.line(self.image,(self.bbox[2]-var, self.bbox[1]) , top_right, color, thickness)
                    cv2.imshow('image', self.image)

                    if cv2.waitKey(1)==ord("q"):
                        break
            video.release()
            cv2.destroyAllWindows()
            self.finish=False
if __name__ =="__main__":
      target_start=Process()


