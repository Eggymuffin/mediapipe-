import json
import paho.mqtt.client as mqtt
import os

BROKER = "broker.hivemq.com"

STATE = {
    "strath/home/light": False,
    "strath/home/door": False,
    "strath/home/alarm": False,
}

STATE_FILE = "state.json"

def read():
    global STATE
    
    if os.path.exists(STATE_FILE):
        
        with open(STATE_FILE, "r") as f:
            STATE = json.load(f)

def save():
    with open(STATE_FILE, "w") as f:
        json.dump(STATE, f)


save()


def on_connect(client, userdata, flags, rc):
    client.subscribe("strath/home/#")
    print("Connected")


def on_message(client, userdata, msg):

    # Synchronize with dashboard
    read()

    payload = msg.payload.decode().strip().upper()

    if payload == "ON":
        STATE[msg.topic] = True
      
    elif payload == "OFF":
        STATE[msg.topic] = False
        
    save()

    print(msg.topic, STATE[msg.topic])


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER)

client.loop_forever()
