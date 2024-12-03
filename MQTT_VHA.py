import paho.mqtt.client as mqtt
import json
import numpy as np
import time

# MQTT Configuration
BROKER = "3.25.112.140"  # IP MQTT của bạn
PORT = 1883
TOPIC = "v2v/collision"

# Generate simulated data for Vehicle A
def generate_vehicle_data(vehicle_id):
    data = {
        "vehicle_id": vehicle_id,
        "x_position": np.random.uniform(0, 100),
        "y_position": np.random.uniform(0, 100),
        "speed": np.random.uniform(20, 100),
        "direction": np.random.uniform(0, 360),
        "timestamp": time.time(),
    }
    return data

# Setup MQTT Client
client = mqtt.Client()

# Connect to Broker
client.connect(BROKER, PORT)

# Publish data for Vehicle A
vehicle_id = "Vehicle_A"
for _ in range(5):  # Simulate sending data 5 times
    vehicle_data = generate_vehicle_data(vehicle_id)
    client.publish(TOPIC, json.dumps(vehicle_data))
    print(f"Sent data: {vehicle_data}")
    time.sleep(2)

# Disconnect after sending
client.disconnect()
