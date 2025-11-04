import paho.mqtt.client as mqtt
import json
import time
import random

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    data = {
        "user_id": "test_user",
        "hrv": random.randint(60, 100),
        "gsr": random.uniform(0.5, 2.0),
        "stress_level": random.randint(1, 10),
        "posture_score": random.randint(50, 100)
    }

    client.publish("neurochair/sensors/test", json.dumps(data))
    print(f"Published: {data}")
    time.sleep(5)
