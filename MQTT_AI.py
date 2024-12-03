import paho.mqtt.client as mqtt
import json
import numpy as np
from sklearn.linear_model import LogisticRegression

# MQTT broker configuration
MQTT_BROKER = "3.25.112.140"
MQTT_PORT = 1883
MQTT_TOPICS = ["V2V_N1/#", "V2V_N2/#", "V2V_N3/#", "V2V_N4/#", "V2V_N5/#"]

# Dữ liệu tạm thời cho từng xe
vehicle_data = {
    "V2V_N1": {},
    "V2V_N2": {},
    "V2V_N3": {},
    "V2V_N4": {},
    "V2V_N5": {}
}

# Huấn luyện mô hình AI (giả định với dữ liệu mẫu)
X_train = np.array([
    [12.25, 5.5, 1.25, 10.12345, 106.7890],
    [15.75, 3.2, 2.5, 10.45678, 106.9876],
    [18.00, 7.0, 0.5, 10.56789, 106.5432]
])
y_train = np.array([1, 1, 0])  # 1 = nguy hiểm, 0 = an toàn

model = LogisticRegression()
model.fit(X_train, y_train)  # Huấn luyện mô hình

# Hàm xử lý khi đủ dữ liệu
def process_vehicle_data(vehicle_id):
    """
    Xử lý khi có đủ dữ liệu từ một xe.
    """
    data = vehicle_data[vehicle_id]

    if all(key in data for key in ["speed", "lidar", "gps"]):
        try:
            # Chuẩn bị dữ liệu cho mô hình
            speed_mps = data["speed"]["data"] * 1000 / 3600  # Chuyển tốc độ sang m/s
            features = np.array([
                speed_mps,
                data["lidar"]["distance"],
                data["gps"]["latitude"],
                data["gps"]["longitude"]
            ])

            # Dự đoán nguy cơ va chạm
            result = predict_collision(features)
            print(f"Collision Prediction for {vehicle_id}: {result}")

            # Gửi cảnh báo nếu nguy cơ cao
            if result == "Collision Risk":
                send_warning(client, f"{vehicle_id}/warning", result)

        except KeyError as e:
            print(f"Error processing vehicle data: Missing {e}")
    else:
        missing_keys = [key for key in ["speed", "lidar", "gps"] if key not in data]
        print(f"Not enough data for {vehicle_id}. Missing: {missing_keys}")

def predict_collision(features):
    """
    Dự đoán nguy cơ va chạm dựa trên mô hình AI.
    """
    prediction = model.predict(features.reshape(1, -1))
    return "Collision Risk" if prediction[0] == 1 else "Safe"

def send_warning(client, topic, message):
    """
    Gửi cảnh báo qua MQTT nếu nguy cơ va chạm cao.
    """
    client.publish(topic, json.dumps({"warning": message}))
    print(f"Warning sent to topic {topic}: {message}")

# Callback khi nhận tin nhắn
def on_message(client, userdata, message):
    try:
        # Phân tích topic để lấy xe và loại dữ liệu
        topic_parts = message.topic.split("/")
        vehicle_id = topic_parts[0]
        data_type = topic_parts[1]

        # Giải mã JSON từ payload
        payload = json.loads(message.payload.decode("utf-8"))

        # Lưu dữ liệu vào dictionary tạm thời
        if vehicle_id in vehicle_data:
            if data_type == "gps":
                vehicle_data[vehicle_id]["gps"] = {
                    "latitude": payload["latitude"],
                    "longitude": payload["longitude"],
                    "timestamp": payload["timestamp"]
                }
            elif data_type in ["speed", "lidar"]:
                vehicle_data[vehicle_id][data_type] = {
                    "data": payload["data"],
                    "unit": payload["unit"],
                    "timestamp": payload["timestamp"]
                }
            else:
                print(f"Ignored data type: {data_type}")

            # Kiểm tra và xử lý nếu đủ dữ liệu
            process_vehicle_data(vehicle_id)

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except KeyError as e:
        print(f"Error processing message: Missing key {e}")

# Callback khi kết nối thành công
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
        for topic in MQTT_TOPICS:
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")
    else:
        print(f"Failed to connect, return code {rc}")

# Log callback để debug nếu cần
def on_log(client, userdata, level, buf):
    print(f"Log: {buf}")

# Cài đặt MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log  # Bật log nếu cần debug chi tiết

# Kết nối tới broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()  # Duy trì kết nối
except Exception as e:
    print(f"Error: {e}")
