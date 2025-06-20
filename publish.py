from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt

load_dotenv()

MQTT_USER = os.getenv("USER")
MQTT_PASS = os.getenv("PASS")


# noinspection PyUnusedLocal
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.username_pw_set(MQTT_USER, MQTT_PASS)
mqttc.connect("xerxes.fritz.box", 1883, 60)
mqttc.publish('mm/test', 'Hello World')
