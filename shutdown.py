#!/usr/bin/env python
import os
import paho.mqtt.client as mqtt
import time

broker = "octopi.local"
port = 1883

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("message =", msg)
    topic = message.topic
    print("Received message on topic:", topic)
    # Execute shutdown command here

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        client.subscribe(sub_topic)
    else:
        client.bad_connection_flag = True
        client.connected_flag = False

# MQTT
sub_topic = "octoprint/shutdownscript"
client = mqtt.Client("Octoprint")
client.on_message = on_message
client.on_connect = on_connect
# client.username_pw_set(username="admin", password="admin")

client.connected_flag = False
try:
    client.connect(broker, port=port)  # Connect to the broker
    client.loop_start()  # Start the MQTT loop

    while client.connected_flag:
        time.sleep(1)  # Your script will continue running here
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting.")
    client.disconnect()
    client.loop_stop()
except Exception as e:
    print(f"An error occurred: {str(e)}")

print("Script finished.")
