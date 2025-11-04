import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
from datetime import datetime

# Connect to MongoDB
mongo_client = MongoClient('mongodb://mongodb:27017/')
db = mongo_client['neurochair']
collection = db['sensor_data']

# MQTT callbacks


def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code {rc}")
    client.subscribe("neurochair/sensors/#")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        data['timestamp'] = datetime.now()
        data['topic'] = msg.topic

        # Store in MongoDB
        collection.insert_one(data)
        print(f"Stored data: {data}")
    except Exception as e:
        print(f"Error: {e}")


# Create MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT broker
mqtt_client.connect("mqtt-broker", 1883, 60)
mqtt_client.loop_forever()
