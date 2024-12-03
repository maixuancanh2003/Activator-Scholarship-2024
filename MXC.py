import numpy as np
import pandas as pd

# Tạo dữ liệu giả lập
np.random.seed(42)
n_samples = 1000

# Tạo các đặc trưng
speed = np.random.uniform(0, 120, n_samples)  # Tốc độ (km/h)
gps_latitude = np.random.uniform(10.0, 10.5, n_samples)  # Vĩ độ
gps_longitude = np.random.uniform(106.0, 106.5, n_samples)  # Kinh độ
lidar_distance = np.random.uniform(1, 50, n_samples)  # Khoảng cách Lidar (m)

# Nhãn mục tiêu: nguy cơ va chạm (1) nếu tốc độ cao và khoảng cách gần
collision = np.where((lidar_distance < 10) & (speed > 40), 1, 0)

# Tạo DataFrame
data = pd.DataFrame({
    "speed": speed,
    "gps_latitude": gps_latitude,
    "gps_longitude": gps_longitude,
    "lidar_distance": lidar_distance,
    "collision": collision
})

# Lưu dữ liệu
data.to_csv("collision_data.csv", index=False)
print("Synthetic data saved to collision_data.csv")
