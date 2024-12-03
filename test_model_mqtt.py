import json
import numpy as np
from tensorflow.keras.models import load_model  # type: ignore
import paho.mqtt.client as mqtt


BROKER_IP = "3.25.112.140"  
PORT = 1883
TOPIC_PREFIX = "V2V_"  # Common prefix for topics
STATUS_TOPIC_PREFIX = "V2V_STATUS/status/"  # Prefix for result topics
NUM_TOPICS = 5  # Number of topics (V2V_N1 to V2V_N5)

# Load the trained model
MODEL_PATH = "collision_detection_model.h5"
model = load_model(MODEL_PATH)
print("Model loaded successfully.")

# Variables to store sensor data for each topic
sensor_data = {f"V2V_N{i}": {"speed": None, "gps_latitude": None, "gps_longitude": None, "lidar_distance": None} for i in range(1, NUM_TOPICS + 1)}

# Function to predict collisions
def predict_collision(sensor_data):
    try:
        # Prepare input for the model
        input_data = np.array([[sensor_data["speed"],
                                sensor_data["gps_latitude"],
                                sensor_data["gps_longitude"],
                                sensor_data["lidar_distance"]]])
        
        # Make a prediction
        prediction = model.predict(input_data)
        if prediction[0][0] > 0.5:
            return "Collision Warning", prediction[0][0]
        else:
            return "Safe", prediction[0][0]
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "Error", 0

# Function to handle messages from MQTT
def on_message(client, userdata, msg):
    global sensor_data
    try:
        # Parse JSON from MQTT
        payload = json.loads(msg.payload.decode())
        topic = msg.topic

        # Determine the main topic (V2V_N1, V2V_N2, ...)
        main_topic = topic.split('/')[0]

        # Ignore if the topic is not in the list of topics to process
        if main_topic not in sensor_data:
            return

        # Update sensor data from subtopics
        if topic.endswith("speed"):
            sensor_data[main_topic]["speed"] = payload.get("data", 0)
        elif topic.endswith("gps"):
            sensor_data[main_topic]["gps_latitude"] = payload.get("latitude", 0)
            sensor_data[main_topic]["gps_longitude"] = payload.get("longitude", 0)
        elif topic.endswith("lidar"):
            sensor_data[main_topic]["lidar_distance"] = payload.get("distance", 0)

        # Perform prediction when all data is available
        if all(value is not None for value in sensor_data[main_topic].values()):
            status, probability = predict_collision(sensor_data[main_topic])
            
            # Publish the warning to MQTT (retain enabled)
            payload = {
                "status": status,
                "probability": float(probability),  # Ensure JSON serializable
                "sensor_data": sensor_data[main_topic]
            }
            status_topic = f"{STATUS_TOPIC_PREFIX}{main_topic}/"
            client.publish(status_topic, json.dumps(payload), retain=True)
            print(f"Published to {status_topic}: {payload}")

            # Reset sensor_data after processing
            sensor_data[main_topic] = {key: None for key in sensor_data[main_topic]}

    except json.JSONDecodeError:
        print(f"Failed to decode JSON from topic {msg.topic}: {msg.payload}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker.")
        # Subscribe to all topics
        for i in range(1, NUM_TOPICS + 1):
            client.subscribe(f"{TOPIC_PREFIX}N{i}/#")
    else:
        print(f"Failed to connect, return code {rc}")

# Configure MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    # Connect to the MQTT broker and listen
    client.connect(BROKER_IP, PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
