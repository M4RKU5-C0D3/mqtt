from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt

load_dotenv()

MQTT_USER = os.getenv("USER")
MQTT_PASS = os.getenv("PASS")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("mm/test") # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.

def on_message(client, userdata, msg):
    print(f"Recieved topic '{msg.topic}' with payload '{msg.payload}'")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(MQTT_USER, MQTT_PASS)
mqttc.connect("xerxes.fritz.box", 1883, 60)
mqttc.loop_start()
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    mqttc.loop_stop()
