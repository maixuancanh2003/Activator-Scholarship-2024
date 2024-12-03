from tensorflow.keras.models import load_model # type: ignore
import numpy as np

model = load_model("collision_detection_model.h5")

new_data = np.array([[60, 10.25364, 106.233, 8.5]])  # speed, latitude, longitude, lidar_distance

prediction = model.predict(new_data)
print("Prediction:", "Collision Warning" if prediction[0][0] > 0.5 else "Safe")
