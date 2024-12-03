import paho.mqtt.client as mqtt
import json
import time

# MQTT Configuration
BROKER = "3.25.112.140"  # IP MQTT của bạn
PORT = 1883
TOPIC = "v2v/collision"

# Define callback for received messages
def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print(f"Received data from {payload['vehicle_id']}: {payload}")

# Setup MQTT Client
client = mqtt.Client()
client.on_message = on_message

# Connect to Broker and subscribe to topic
client.connect(BROKER, PORT)
client.subscribe(TOPIC)

# Start a loop to keep receiving data
print("Listening for messages...")
client.loop_start()

# Keep the script running to receive messages
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting...")
    client.loop_stop()
    client.disconnect()
