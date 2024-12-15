"""
WSGI config for iot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application
import os
import json
import paho.mqtt.client as mqtt
import threading
import time
from user_interface.models import *
from data_collect.models import *
from .task import *
broker_address='127.0.0.1'
port=1883
# Define the MQTT callback functions for 'order' and 'order1' topics

def on_connect(client, userdata, flags, rc):
    client.subscribe('data_topic')  # Subscribe to the 'order1' topic
    print("Subscribing to topic: tempurature_topic")

def on_message(client, userdata, msg):
    try:
        received_data = json.loads(msg.payload.decode())
        print(received_data)
        tempurature = received_data["temperature"]
        himidity = received_data["himidity"]
        waterLevel = received_data["waterLevel"]
        print('----------------------------------------pass')
        print(msg.topic+" "+str(msg.payload))
        tempurature = float(tempurature)  
        himidity = float(himidity)  
        waterLevel = float(waterLevel)  
        Tempurature.objects.create(tempurature=tempurature)  
        Himidity.objects.create(himidity=himidity)  
        WaterLevel.objects.create(waterlevel=waterLevel)  
        # Handle 'order1' message here
    except :
        print ('-------------------------------------------------- error handeling data values ---------------------')
        pass
def subscribe(client, on_connect_callback):
    client.on_connect = on_connect_callback
    client.on_message = on_message
    
    client.connect(broker_address, port,keepalive=60)
    client.loop_forever()

# Initialize the MQTT clients
client = mqtt.Client(client_id='client_9')
client1 = mqtt.Client(client_id='client_100')
t = threading.Thread(target=subscribe, args=(client, on_connect))

t3=threading.Thread(target=receive_and_process_session_data)
t4=threading.Thread(target=send_session_data)
t5=threading.Thread(target=send_control_settings_data)
t6=threading.Thread(target=receive_and_process_control_settings)
t6.start()
t5.start()
t4.start()
t3.start()
t.start()

# print(timezone.now().strftime(f"%Y-%m-%d %H:%M:00+00:00 "))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iot.settings')
application = get_wsgi_application()
