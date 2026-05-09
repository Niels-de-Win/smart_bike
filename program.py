import cv2
import face_recognition
import numpy as np
import time
import os

class FaceRecognizer:
    def __init__(self, reference_images):
        self.reference_data = {}
        self.last_detected_name = None

        for name, path in reference_images.items():
            try:
                if not os.path.exists(path):
                    print(f"WARNING: File {path} not found, skipping {name}")
                    continue
                img = face_recognition.load_image_file(path)
                img = np.ascontiguousarray(img)
                if img.dtype != np.uint8:
                    img = img.astype(np.uint8)
                
                print(f"DEBUG: {path} loaded.")
                encodings = face_recognition.face_encodings(img)
                
                if encodings:
                    self.reference_data[name] = encodings[0]
                    print(f"SUCCESS: Added {name} to system.")
                else:
                    print(f"WARNING: No face found in {path}, skipping {name}")
            except Exception as e:
                print(f"ERROR: Could not load {path}: {str(e)}")

    def recognize(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        current_frame_name = None
        for face_encoding in face_encodings:
            name = "Unknown"
            best_distance = 1.0
            for ref_name, ref_enc in self.reference_data.items():
                distance = face_recognition.face_distance([ref_enc], face_encoding)[0]
                if distance < 0.6 and distance < best_distance:
                    best_distance = distance
                    name = ref_name
            current_frame_name = name

        self.last_detected_name = current_frame_name
        return frame

def main():
    people = {
        "Gyokmen": "gyokmen.jpg",
        "Veerle":  "veerle.jpg",
        "Niels":   "niels.jpg",
        "Maxim":   "maxim.jpg"
    }

    recognizer = FaceRecognizer(people)
    if not recognizer.reference_data:
        print("ERROR: No reference images found.")
        return

    # SETTINGS
    # Load IP from .env file
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    phone_ip = "192.168.1.22"  # fallback default
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("PHONE_IP="):
                    phone_ip = line.strip().split("=", 1)[1]
                    break

        PHONE_STREAM_URL = f"http://{phone_ip}:4747/video"
        is_phone_stream = True

    # 1st Attempt: Phone Camera
    print(f"Attempting to connect to phone: {PHONE_STREAM_URL}...")
    cap = cv2.VideoCapture(PHONE_STREAM_URL)

    # 2nd Attempt: Laptop Camera (Backup)
    if not cap.isOpened():
        print("WARNING: Could not connect to phone. Switching to Laptop Camera...")
        cap = cv2.VideoCapture(0)
        is_phone_stream = False
        
    if not cap.isOpened():
        print("ERROR: No cameras available at all.")
        return False

    print(f"\n--- System Started ({'Phone' if is_phone_stream else 'Laptop'} Camera) ---")
    
    detected_face_start_time = None
    detected_name = None

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Rotate ONLY if using the phone stream (Landscape -> Portrait)
            if is_phone_stream:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            recognizer.recognize(frame)
            current_name = recognizer.last_detected_name

            if current_name and current_name != "Unknown":
                if detected_name != current_name:
                    detected_name = current_name
                    detected_face_start_time = time.time()
                    print(f"MATCH: {detected_name} found!")
                else:
                    if time.time() - detected_face_start_time >= 1:
                        print(f"\n***************************")
                        print(f"*** WELCOME, {detected_name.upper()}! ***")
                        print(f"***************************\n")
                        cap.release()
                        time.sleep(3)
                        return True
            else:
                detected_name = None
                detected_face_start_time = None

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        if cap.isOpened():
            cap.release()
        print("--- System Closed ---")

if __name__ == "__main__":
    main()
