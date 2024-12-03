import paho.mqtt.client as mqtt
import json
import numpy as np
from tensorflow.keras.models import load_model

# MQTT broker settings
BROKER_IP = "3.25.112.140"
PORT = 1883
TOPIC = "V2V_N2/#"
STATUS_TOPIC = "V2V_N2/status"

# Load pretrained AI model
MODEL_PATH = "Accident_Detection_Model.h5"  # Đường dẫn đến mô hình đã huấn luyện
model = load_model(MODEL_PATH)

# Global variables for storing sensor data
sensor_data = {
    "speed": None,
    "gps_latitude": None,
    "gps_longitude": None,
    "lidar_distance": None,
    "steering_angle": None,
    "tilt": None
}

# Callback function when connecting to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker!")
        client.subscribe(TOPIC)
    else:
        print("Failed to connect, return code %d\n", rc)

# Analyze data using the AI model
def analyze_with_ai(data):
    # Convert data to model input format
    input_data = np.array([[data["speed"], data["gps_latitude"], data["gps_longitude"], 
                            data["lidar_distance"], data["steering_angle"], data["tilt"]]])
    
    # Predict with the model
    prediction = model.predict(input_data)
    if prediction[0][0] > 0.5:
        return "Collision Warning"
    else:
        return "Safe"

# Callback function for processing messages
def on_message(client, userdata, msg):
    try:
        # Parse the JSON data
        payload = json.loads(msg.payload.decode())
        topic = msg.topic

        # Map the data to the appropriate sensor
        if topic.endswith("speed"):
            sensor_data["speed"] = payload.get("data", 0)
        elif topic.endswith("gps"):
            sensor_data["gps_latitude"] = payload.get("latitude", 0)
            sensor_data["gps_longitude"] = payload.get("longitude", 0)
        elif topic.endswith("lidar"):
            sensor_data["lidar_distance"] = payload.get("distance", 0)
        elif topic.endswith("steering_angle"):
            sensor_data["steering_angle"] = payload.get("data", 0)
        elif topic.endswith("tilt"):
            sensor_data["tilt"] = payload.get("data", 0)

        # Check if all data fields are filled
        if all(value is not None for value in sensor_data.values()):
            # Analyze with AI model
            status = analyze_with_ai(sensor_data)

            # Publish the status to MQTT
            status_payload = {"status": status, "sensor_data": sensor_data}
            client.publish(STATUS_TOPIC, json.dumps(status_payload))
            print(f"Published status: {status_payload}")

            # Reset sensor data after processing
            for key in sensor_data.keys():
                sensor_data[key] = None

    except json.JSONDecodeError:
        print(f"Failed to decode JSON from topic {msg.topic}: {msg.payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Set up MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
try:
    client.connect(BROKER_IP, PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
