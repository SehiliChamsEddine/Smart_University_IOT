

from copy import deepcopy
#-------------------------------------------------
import paho.mqtt.client as mqtt
import json
import time
from django.utils import timezone
from user_interface.models import SetSession, Student, Teacher, Attendance
from data_collect.models import *
broker_address='127.0.0.1'
port=1883

def send_session_data(broker_address=broker_address,port=port):
    all_students=''
    client = mqtt.Client(client_id="45767879")
 
    while True:
        current_time = timezone.now().strftime(f"%Y-%m-%d %H:%M:00+00:00")  # Format current time to match SetSession's time format
        print(current_time)
        try:
            session = SetSession.objects.get(time=current_time)
            students = Student.objects.filter(group_number=session.group)
            teacher = session.teacher
            class_name = session.class_name
            print('performed')
            print(students)
        except SetSession.DoesNotExist:
            # No active session
            print("error")
            time.sleep(5)  # Sleep for 1 minute and check again
            continue
        for student in students :
             all_students += student.id_number+' '
        # Create a JSON object with session data
        data = {
            "time": current_time,
            "students": all_students,
            "teacher": teacher.id_number,
            "class_name": class_name,
        }
        print(data)
        send=json.dumps(data)
        client.connect(broker_address, port)
        # Send the JSON session data to Raspberry Pi via MQTT
        for i in range(2):
             client.publish("session_data0",send)
        time.sleep(56)  # Sleep for 1 minute before checking again
        client.disconnect()
        all_students=''


#-------------------------------------------------------------------------


def receive_and_process_session_data(broker_address=broker_address,port=port):
    def on_message(client, userdata, message):
        try:
            received_data = json.loads(message.payload.decode())
            teacher_id = received_data["teacher"]
            student_ids = received_data["students"]
            session_time = received_data["time"]

            if session_time:
                session=SetSession.objects.get(time=session_time)
                print('find_time')
            if student_ids :

                        student_list=student_ids.lstrip().rstrip().split(' ')
                        print(student_list)
                
            # Retrieve the teacher and students
                        students = Student.objects.filter(id_number__in=student_list)
                    # Process the received data and create attendance records

                        for student in students:
                                    Attendance.objects.create(session=session,student=student)
                                    print('done')
                
            if teacher_id:
                teacher = Teacher.objects.get(id_number=teacher_id)
                Attendance.objects.create(session=session,teacher=teacher)
                print('done')
        except:
            print('error')
    client = mqtt.Client(client_id='1354614613')
    client.on_message = on_message
    client.connect(broker_address, port)
    client.subscribe("session_data_recive")
    client.loop_forever()

#  -----------------------------------------------------------------------   controle settings 




def send_control_settings_data(broker_address="127.0.0.1", port=1883):
    print(f"Connecting to broker at {broker_address}:{port}...")
    client = mqtt.Client(client_id="control_settings_sender")

    try:
 
        last_known_settings = {}

        while True:
            try:    
                control_settings = ControlSettingsPublish.objects.last()
                current_settings = {
                    'water_pump_status': control_settings.water_pump_status,
                    'block1_status': control_settings.block1_status,
                    'block2_status': control_settings.block2_status,
                    'block3_status': control_settings.block3_status,
                    
                }

                if current_settings != last_known_settings:
                    client.connect(broker_address, port)
                    print(f"Connected to broker at {broker_address}:{port}")
                    last_known_settings = deepcopy(current_settings)
                    send = json.dumps(current_settings)

                    client.publish("control_settings_publish", send)
                    time.sleep(2)
                    print(f"Sent control settings: {current_settings}")
                    client.disconnect()
                    

                
            except Exception as e:
                print(f"Error sending control settings data: {str(e)}")
                time.sleep(5)
    except Exception as e:
        print(f"Error connecting to broker: {str(e)}")
# ... Existing code ...
def receive_and_process_control_settings(broker_address=broker_address,port=port):
    control_settings_data = {}
    
    control_settings = ControlSettingsRecive.objects.first()
  
   
    def on_message(client, userdata, message):
        try:
           

            received_data = json.loads(message.payload.decode())
            control_settings_data["block1_status"] = received_data.get("block1_status")
            control_settings_data["block2_status"] = received_data.get("block2_status")
            control_settings_data["block3_status"] = received_data.get("block3_status")
            control_settings_data["fire_detection"] = received_data.get("fire_detection")
            control_settings_data["gas_detection"] = received_data.get("gas_detection")
            control_settings_data["water_pump_status"] = received_data.get("water_pump_status")
           
            
            if control_settings:
                # Update the ControlSettings1 object with the received data
                control_settings.block1_status = control_settings_data.get("block1_status")
                control_settings.block2_status = control_settings_data.get("block2_status")
                control_settings.block3_status = control_settings_data.get("block3_status")
                control_settings.fire_detection = control_settings_data.get("fire_detection")
                control_settings.gas_detection = control_settings_data.get("gas_detection")
                control_settings.water_pump_status = control_settings_data.get("water_pump_status")
          
                
                # Save the changes to the database
                control_settings.save()

                print("Updated control settings:", control_settings_data)
                
        except Exception as e:
            print(f"Error processing control settings data: {str(e)}")

    client = mqtt.Client(client_id='control_settings_receiver')
    client.on_message = on_message
    client.connect(broker_address, port)
    client.subscribe("control_settings_recive")
    client.loop_forever()








# Function to send control settings data
# def send_control_settings_data(broker_address=broker_address,port=port):
#     client = mqtt.Client(client_id="control_settings_sender")
#     client.connect(broker_address, port)
#     last_known_controle_settings = ControlSettings.objects.all()  # Store the last known control settings
#     last_known_settings={}
#     for known_settings in last_known_controle_settings:
#                 last_known_settings['light1_status'] = known_settings.light1_status
#                 last_known_settings['light2_status'] = known_settings.light2_status
#                 last_known_settings['light3_status'] = known_settings.light3_status
#                 last_known_settings['light4_status'] = known_settings.light4_status
#                 last_known_settings['light5_status'] = known_settings.light5_status
#                 last_known_settings['water_pump_status'] = known_settings.water_pump_status
#     d=0
#     while True:
#         try:
#             # Retrieve control settings from the database
#             control_settings = ControlSettings.objects.first()
#             current_settings = {}

            
#             current_settings['light1_status'] = control_settings.light1_status
#             current_settings['light2_status'] = control_settings.light2_status
#             current_settings['light3_status'] = control_settings.light3_status
#             current_settings['light4_status'] = control_settings.light4_status
#             current_settings['light5_status'] = control_settings.light5_status
#             current_settings['water_pump_status'] = control_settings.water_pump_status
                

#             # Check if the settings have changed
#             if current_settings != last_known_settings or d == 0:
#                 d+=1
#                 print(current_settings)
#                 last_known_settings=deepcopy(current_settings)
#                 print(type(last_known_settings['light2_status']))
#                 time.sleep(0.5)
#             #     # Create a JSON object with control settings data
#             #     data = {
#             #         "control_settings": current_settings
#             #     }
#                 send = json.dumps(current_settings)

#             #     # Send the JSON control settings data to Raspberry Pi via MQTT
#                 client.publish("controle_settings1", send)
#                 time.sleep(0.5)

#             #     # Update last_known_settings
#             #     last_known_settings = current_settings

#                 print(f"Sent control settings: {current_settings}")

#             time.sleep(0.2)  # Sleep for 1 minute before checking again
#         except Exception as e:
#             print(f"Error sending control settings data: {str(e)}")
#             time.sleep(1)  # Sleep for 5 seconds before checking again

