from ultralytics import YOLO
import cv2
import paho.mqtt.client as mqtt
import time
import easyocr
import json

# Initialize MQTT client
client = mqtt.Client(client_id="587364535763")

# List of authorized license plate numbers
authorized_plates = ['1773711116', '0365510842', '00866112116']

# Parking location status
parking_location = {
    1: '',
    2: ''
   }
# Load models
model = YOLO('Yolobest.pt')
reader = easyocr.Reader(['en'], gpu=True)

# Load video
cap = cv2.VideoCapture(0)


def process_frame(frame):
    """
    Process a single video frame to detect and read license plates.
    """
    results = model(frame)
    detections = results[0].boxes
    for box in detections:
        x1, y1, x2, y2 = [int(i) for i in box.xyxy[0]]
        license_plate_crop = frame[y1:y2, x1:x2, :]
        license_plate_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)

        result = reader.readtext(license_plate_gray)
        if result:
            text = result[0][-2].strip().replace(' ', '')
            if text in authorized_plates:
                message = assign_parking_location(text)
                if message:
                    send_mqtt_message("artificial", message)

            # Annotate the frame with the detected license plate number
            cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        
        # Draw the bounding box on the frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

    return frame


def send_mqtt_message(topic, message):
    """
    Send a message via MQTT.
    """
    try:
        client.connect('127.0.0.1', 1883)
        client.publish(topic, json.dumps(message))
        time.sleep(2)
        client.disconnect()
    except Exception as e:
        print(f"Error sending MQTT message: {e}")


def assign_parking_location(license_plate):
    """
    Assign a detected license plate to an available parking location.
    If the license plate is already assigned, remove it (car leaving).
    """
    for spot, plate in parking_location.items():
        if plate == license_plate:
            parking_location[spot] = ''
            print(f"Car with license plate {license_plate} left parking spot {spot}")
            return {"car_out": True}
    
    for spot, plate in parking_location.items():
        if plate == '':
            parking_location[spot] = license_plate
            print(f"Assigned {license_plate} to parking spot {spot}")
            return {"car_on": True, "Park_number": spot}
    
    print("No available parking spots")
    return {"car_on":False ,"Park_number": "not available"}


def main():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_frame = process_frame(frame)
        cv2.imshow('Processed Video', processed_frame)
        
        if cv2.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
