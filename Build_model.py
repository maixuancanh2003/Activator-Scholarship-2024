import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense 

# Read data
data = pd.read_csv("collision_data.csv")
X = data[["speed", "gps_latitude", "gps_longitude", "lidar_distance"]]
y = data["collision"]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the model
model = Sequential([
    Dense(64, input_dim=4, activation='relu'),  # 4 input features
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # Predict collision probability
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_test, y_test))

# Save the model
model.save("collision_detection_model.h5")
print("Model saved as collision_detection_model.h5")
