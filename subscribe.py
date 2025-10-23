import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from dbus_notification import DBusNotification

load_dotenv()

MQTT_USER = os.getenv("USER")
MQTT_PASS = os.getenv("PASS")
MQTT_HOST = os.getenv("HOST")


# noinspection PyUnusedLocal
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("zigbee2mqtt/Präsenz - Markus Zimmer")  # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.


def callback(notification_type, notification):
    if notification_type == "closed":
        print(f"Notification {notification['id']} has closed.")
    elif notification_type == "button":
        print(f"Notification {notification['id']} has clicked on the button {notification['button']}.")


# noinspection PyUnusedLocal
def on_message(client, userdata, msg):
    import json
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        presence = data.get('presence')
        motion_state = data.get('motion_state')
        print({'presence': presence, 'motion_state': motion_state})
        message = f"presence: {presence}, motion_state: {motion_state}"
    except Exception as e:
        print(f"Fehler beim Verarbeiten des Payloads: {e}")
        message = "Ungültiges Payload"

    DBusNotification(appname="dbus_notification", callback=callback).send(
        title="MQTT",
        message=message,
        logo="/usr/share/icons/Yaru/16x16/status/dialog-warning.png",
        image="/usr/share/icons/Yaru/16x16/status/dialog-information.png",
        sound="/usr/share/sounds/gnome/default/alerts/hum.ogg",
        actions=["Yes","No"],
        urgency=1,
        timeout=100,
    )


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(MQTT_USER, MQTT_PASS)
mqttc.connect(MQTT_HOST, 1883, 60)
mqttc.loop_start()
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    mqttc.loop_stop()
