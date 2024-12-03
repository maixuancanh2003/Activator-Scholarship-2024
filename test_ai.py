import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

# Calculate features: distance and speed difference
df["distance"] = np.sqrt((df["x2"] - df["x1"]) ** 2 + (df["y2"] - df["y1"]) ** 2)
df["speed_diff"] = abs(df["speed1"] - df["speed2"])

# Features and labels
features = df[["distance", "speed_diff"]]
labels = df["collision"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Test with a new data point
test_data = pd.DataFrame({
    "distance": [10, 50],
    "speed_diff": [20, 5]
})
collision_prob = model.predict_proba(test_data)

print("\nTest Data Predictions:")
for i, prob in enumerate(collision_prob):
    print(f"Sample {i+1} - Probability of Collision: {prob[1]:.2f}")
