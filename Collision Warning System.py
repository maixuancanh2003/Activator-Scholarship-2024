# Collision Warning System
import paho.mqtt.client as mqtt
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# MQTT Config
BROKER = "3.25.112.140"  # IP MQTT của bạn
PORT = 1883
TOPIC = "v2v/collision"

# Random Forest Model Placeholder
model = None

# Callback for receiving messages
def on_message(client, userdata, message):
    global model
    payload = json.loads(message.payload.decode())
    print(f"Received data from {payload['vehicle_id']}: {payload}")
    
    # Process the received data
    vehicle_data = {
        "x_position": payload["x_position"],
        "y_position": payload["y_position"],
        "speed": payload["speed"],
        "direction": payload["direction"]
    }
    
    # Simulate collision check
    other_vehicle = generate_vehicle_data("Vehicle_B")  # Placeholder for another vehicle
    collision_risk = predict_collision(vehicle_data, other_vehicle)
    print(f"Collision Risk: {collision_risk:.2f}")

# Setup MQTT Client
client = mqtt.Client()
client.on_message = on_message

# Connect to MQTT Broker
client.connect(BROKER, PORT)
client.subscribe(TOPIC)
client.loop_start()

# Function to simulate vehicle data
def generate_vehicle_data(vehicle_id):
    data = {
        "vehicle_id": vehicle_id,
        "x_position": np.random.uniform(0, 100),
        "y_position": np.random.uniform(0, 100),
        "speed": np.random.uniform(20, 100),
        "direction": np.random.uniform(0, 360)
    }
    return data

# Function to predict collision risk
def predict_collision(vehicle_1, vehicle_2):
    global model
    distance = np.sqrt((vehicle_1["x_position"] - vehicle_2["x_position"])**2 +
                       (vehicle_1["y_position"] - vehicle_2["y_position"])**2)
    speed_diff = abs(vehicle_1["speed"] - vehicle_2["speed"])
    angle_diff = abs(vehicle_1["direction"] - vehicle_2["direction"])
    
    # Prepare features
    features = pd.DataFrame([[distance, speed_diff, angle_diff]], columns=["distance", "speed_diff", "angle_diff"])
    
    # Predict collision risk
    risk = model.predict_proba(features)[0][1]
    return risk

# Train Random Forest Model
def train_model():
    global model
    np.random.seed(42)
    n_samples = 1000
    data = {
        "x1": np.random.uniform(0, 100, n_samples),
        "y1": np.random.uniform(0, 100, n_samples),
        "x2": np.random.uniform(0, 100, n_samples),
        "y2": np.random.uniform(0, 100, n_samples),
        "speed1": np.random.uniform(20, 100, n_samples),
        "speed2": np.random.uniform(20, 100, n_samples),
        "collision": np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2])
    }
    df = pd.DataFrame(data)
    df["distance"] = np.sqrt((df["x2"] - df["x1"])**2 + (df["y2"] - df["y1"])**2)
    df["speed_diff"] = abs(df["speed1"] - df["speed2"])
    df["angle_diff"] = abs(np.random.uniform(0, 180, n_samples))
    
    X = df[["distance", "speed_diff", "angle_diff"]]
    y = df["collision"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    print(f"Model trained with accuracy: {accuracy * 100:.2f}%")

# Train the model
train_model()
