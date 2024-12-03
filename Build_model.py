import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Đọc dữ liệu
data = pd.read_csv("collision_data.csv")
X = data[["speed", "gps_latitude", "gps_longitude", "lidar_distance"]]
y = data["collision"]

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Xây dựng mô hình
model = Sequential([
    Dense(64, input_dim=4, activation='relu'),  # 4 đặc trưng đầu vào
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # Dự đoán xác suất va chạm
])

# Biên dịch mô hình
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình
model.fit(X_train, y_train, epochs=20, batch_size=16, validation_data=(X_test, y_test))

# Lưu mô hình
model.save("collision_detection_model.h5")
print("Model saved as collision_detection_model.h5")
