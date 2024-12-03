import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Generate simulated dataset
np.random.seed(42)
n_samples = 1000
data = {
    "x1": np.random.uniform(0, 100, n_samples),
    "y1": np.random.uniform(0, 100, n_samples),
    "x2": np.random.uniform(0, 100, n_samples),
    "y2": np.random.uniform(0, 100, n_samples),
    "speed1": np.random.uniform(20, 100, n_samples),
    "speed2": np.random.uniform(20, 100, n_samples),
    "collision": np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2]),  # 20% collision
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate features: distance, speed difference, and angle difference
df["distance"] = np.sqrt((df["x2"] - df["x1"]) ** 2 + (df["y2"] - df["y1"]) ** 2)
df["speed_diff"] = abs(df["speed1"] - df["speed2"])
df["angle_diff"] = abs(np.random.uniform(0, 180, n_samples))  # Simulated angle difference

# Features and labels
features = df[["distance", "speed_diff", "angle_diff"]]
labels = df["collision"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Define Neural Network model
model = Sequential([
    Dense(32, input_dim=3, activation='relu'),  # Input layer
    Dense(16, activation='relu'),              # Hidden layer
    Dense(1, activation='sigmoid')             # Output layer (probability)
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test), verbose=1)

# Evaluate the model
accuracy = model.evaluate(X_test, y_test, verbose=0)[1]
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Test with a new data point
test_data = np.array([[10, 20, 30], [50, 10, 70]])  # Example inputs: [distance, speed_diff, angle_diff]
predictions = model.predict(test_data)
print("\nTest Data Predictions:")
for i, prob in enumerate(predictions):
    print(f"Sample {i+1} - Probability of Collision: {prob[0]:.2f}")
