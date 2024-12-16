# AI Powered V2V Safety

## Overview
"AI Powered V2V Safety" is a cutting-edge project designed to enhance vehicle safety through Vehicle-to-Vehicle (V2V) communication using AI technology. Utilizing an ESP32 microcontroller, the system gathers data from multiple sensors: GPS (NEO-6MV2), Lidar (TF Luna Mini), and Radar (HLK-LD1115H). This data is then stored in Excel file format on an SD card and transmitted as JSON to a PC server for processing.

## System Architecture
The system processes sensor data using a TensorFlow Keras model, `collision_detection_model.h5`, to assess safety conditions. Processed data is transmitted back to vehicles via an MQTT broker, ensuring real-time safety alerts during vehicular movement.

### Key Components
- **Microcontroller:** ESP32
- **Sensors:** GPS, Lidar, Radar
- **Data Handling:** JSON format, Excel storage
- **AI Model:** TensorFlow Keras (`collision_detection_model.h5`)
- **Communication:** MQTT broker (IP: 3.25.112.140, Port: 1883)
- **Server Hardware:** Intel Core i5, ASUS VivoBook

## Installation and Setup
1. Set up ESP32 with sensors and ensure correct wiring.
2. Configure MQTT broker settings on ESP32.
3. Load the AI model onto your server from the provided files.
4. Ensure your server's IP and port settings match those configured for MQTT.
5. Start the system and monitor outputs for safety evaluations.

## Usage
Connect to the MQTT broker using the IP address provided to receive real-time updates on vehicle safety statuses. This allows for monitoring and further analysis of the V2V communication effectiveness.

## Resources
- Video Demonstration: [Demo Video](Video\Demo.mp4)
- Images:
  - MQTT Setup: ![MQTT Setup](Image\MQTT.png)
  - Results Display: ![Results Display](Image\RESULT.png)
  - Hardware: ![Top View](Image\TOP.png)

## Contact
For any questions or additional support, feel free to reach out:

- **Name:** Mai Xuan Canh
- **University:** Ho Chi Minh City University of Technology (HCMUT)
- **Major:** Control and Automation Engineering
- **LinkedIn:** [Canh Mai's LinkedIn](https://www.linkedin.com/in/maixuancanh2003/)
- **Email:** canhmai.work@gmail.com