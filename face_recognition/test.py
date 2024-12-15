import face_recognition
import cv2
import numpy as np
import os
names = np.array([], dtype=object)
faces=[]


for image in os.listdir('faces'):
      face=cv2.imread(f"faces/{image}")
      encodings=face_recognition.face_encodings(face)[0]

      faces.append(encodings)
      print(len(faces))
      names=np.append(names,image.split('.')[0])
# Load the image
image_path = "chams.jpg"
image = cv2.imread(image_path)

# Convert the image from BGR color (OpenCV) to RGB color (face_recognition)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect face locations
face_locations = face_recognition.face_locations(rgb_image)
encoding=face_recognition.face_encodings(rgb_image,face_locations)
print(encoding)
comparition=face_recognition.compare_faces(faces,encoding[0])
name_check=names[comparition]
print(name_check)
# Loop through each detected face and draw bounding box
(top, right, bottom, left )= face_locations[0]
    # Draw a rectangle around the face
cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

# Display the image with bounding boxes
cv2.imshow("Detected Faces", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
