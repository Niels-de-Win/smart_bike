# 🚲 Smart Bike Lock & Dashboard (AI Face Recognition)

A high-performance AI-powered project for **Raspberry Pi 5**. This system secures your bike using facial recognition and provides a real-time riding dashboard with collision warnings.

## 🚀 Key Features
- **AI Facial Recognition**: High-accuracy detection using `dlib`. Automatically loads authorized users from `.jpg` files in the project folder.
- **Riding Dashboard**: Post-authentication dashboard showing real-time speed (**KM/H**) and system status.
- **Collision Warning System**: Uses an **HC-SR04 Ultrasonic Sensor** to monitor proximity. If an object is closer than 30cm, it triggers a **Buzzer Alarm** and a visual warning on the OLED.
- **Dual Camera Failover**: Automatically switches from the primary Phone camera stream (Wi-Fi) to the laptop's USB camera if the phone is disconnected.
- **OLED UI (SSD1306)**: Premium interface with custom layouts for "Locked", "Welcome", and "Dashboard" states.
- **Cross-Platform Testing**: Fully supports **Mock GPIO, Display, and Sensors**, allowing development and testing on any PC without physical hardware.

## 🛠️ Installation & Setup

### 1. Fast Setup
Run the automated setup script:
```bash
bash setup.sh
```
This script creates a virtual environment, installs all dependencies, and configures your network settings.

### 2. Add Users
Drop `.jpg` photos of authorized people into the root directory. Name the files after the people (e.g., `niels.jpg`). They will be authorized automatically.

## 🔌 Hardware Configuration (Pi 5)
- **Stepper Motor**: GPIO 14, 15, 18, 23
- **OLED Display (SPI)**: DC=24, RES=25, CS=5, SCK=Clock, MOSI=Data
- **Ultrasonic Sensor**: Trig=27, Echo=17
- **Buzzer**: GPIO 22
- **Lock Button**: GPIO 16

## 🏃 Usage
Start the system with:
```bash
bash quicklaunch.sh
```

## 📂 Project Structure
- `lock.py`: Main logic, hardware management, and dashboard controller.
- `program.py`: Facial recognition engine (auto-loads users).
- `display_manager.py`: OLED interface management.
- `setup.sh` / `quicklaunch.sh`: Environment and startup scripts.

---
*Created for IoT Essentials @ Thomas More.*
