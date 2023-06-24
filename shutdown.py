#!/usr/bin/env python
import os
import sys
import paho.mqtt.client as mqtt
import time
broker="octopi.local"
port=1833

#define callback
def on_message(client, userdata, message):
   msg=str(message.payload.decode("utf-8"))
   print("message =",msg)
   topic=message.topic
   messages.append([topic,msg])
def on_connect(client, userdata, flags,rc):
    if rc==0:
        client.connected_flag=True
        client.subscribe(sub_topic)
    else:
        client.bad_connection_flag=True
        client.connected_flag=False

## MQTT
messages=[]
sub_topic="octoprint/shutdown"
client= mqtt.Client("Octoprint")
######
client.on_message=on_message
client.on_connect=on_connect
## client.username_pw_set(username="admin", password="admin")
client.connected_flag=False
client.connect(broker, port=port)#connect
while True:
   client.loop(0.01)
   time.sleep(1)
   if len(messages)>0:
      m=messages.pop(0)
      print("shutdown")
      client.publish("sonoff/mains", payload=None, qos=0, retain=False)
      os.system("sudo shutdown now")
