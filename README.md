# IoT AI Face Recognition Lock

A Python-based face recognition-based lock designed to run on **Raspberry Pi 5**. It uses a mobile phone (via DroidCam or IP Webcam) as a wireless camera stream and features an automatic backup to the laptop's built-in camera. This opens the lock, allowing the bike to drive.

## 🚀 Features
- **Cross-Platform:** The system can run fully autonimous on a raspberry pi, as long as it has been set up on the network.
- **Wireless Stream:** Uses your phone as a high-quality Wi-Fi camera.
- **Auto-Failover:** Automatically switches to the laptop camera if the phone stream is unavailable as long as it is connected.
- **Portrait Support:** Automatically rotates phone streams to portrait mode for better face detection.
- **Headless Optimized:** Designed to run via SSH without needing a monitor.
- **Automated Setup:** It is easy to set up, simply requiring to run a single bash file.

## 🛠️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Reference Images
Add your reference photos (e.g., `gyokmen.jpg`) to the root folder. The system will load them automatically on startup.

### 3. Connect Phone Camera
- Open **DroidCam** or **IP Webcam** on your phone.
- Run the setup.sh file on the pc to set the wifi connection and phone ip.

## 🏃 Running the System
```bash
~/Smart_Bike/setup.sh
```

## 📝 Configuration
In `program.py`, you can adjust:
- `distance < 0.6`: Sensitivity of recognition (lower is stricter).
- `cv2.ROTATE_90_CLOCKWISE`: Change rotation if your phone orientation is different.

---
*Created for IoT Essentials @ Thomas More.*
