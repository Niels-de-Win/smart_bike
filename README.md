# 🚲 Smart Bike Lock (AI Face Recognition)

A professional AI-powered face recognition lock system designed for **Raspberry Pi 5**. This project secures a bike using a stepper motor lock and authenticates users via facial recognition.

## 🚀 Key Features
- **Facial Recognition**: High-accuracy face detection and recognition using `dlib` and `face_recognition`.
- **Dual Camera Support**: 
  - Primary: Wireless phone stream (via DroidCam/IP Webcam).
  - Backup: Laptop/USB camera failover.
- **Collision Warning System**: Uses an **HC-SR04 Ultrasonic Sensor** to monitor objects in front of the bike. If something gets closer than 30cm, the system triggers a **Buzzer Alarm** and visual warning.
- **Visual Feedback**: Real-time status and welcome messages on a **SSD1306 OLED Display** (SPI).
- **Physical Lock**: Stepper motor control for robust locking/unlocking.
- **Cross-Platform Testing**: Built-in **Mock GPIO and Display** systems allow you to test the entire logic on a laptop without physical hardware.
- **Automated Setup**: Interactive setup script for WiFi and IP configuration.

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have Python 3 installed. This project is optimized for Raspberry Pi OS but runs on Linux/macOS for testing.

### 2. Fast Setup
Clone the repository and run the setup script:
```bash
bash setup.sh
```
This script will:
- Create a Python virtual environment.
- Install all necessary dependencies (OpenCV, dlib, Adafruit Blinka, etc.).
- Prompt for your WiFi and Phone IP settings.

### 3. Add Authorized Users
Simply drop `.jpg` files of authorized people into the root directory (e.g., `niels.jpg`). The system will automatically detect and load them as authorized users.

## 🏃 Usage

### Quick Launch
To start the system with existing settings:
```bash
bash quicklaunch.sh
```

### Configuration
You can modify `.env` to change your Phone's IP address or re-run `setup.sh`.

## 📂 Project Structure
- `lock.py`: Main controller handling the state machine, GPIO, and lock logic.
- `program.py`: Facial recognition engine and camera management.
- `display_manager.py`: OLED UI management and English-translated display logic.
- `setup.sh`: Automated environment setup and configuration.
- `quicklaunch.sh`: Fast startup script.

---
*Created for IoT Essentials @ Thomas More.*
