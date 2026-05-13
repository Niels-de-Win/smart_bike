import program
from time import sleep
import os
import random
from display_manager import DisplayManager

# Try to import gpiozero, fallback to a mock if not on a Raspberry Pi
try:
    from gpiozero import DigitalOutputDevice, Button, DistanceSensor, TonalBuzzer
    from gpiozero.devices import Device
    Device.ensure_pin_factory()
    HAS_GPIO = True
except (ImportError, Exception):
    print("WARNING: gpiozero could not find a pin factory. Using Mock GPIO.")
    HAS_GPIO = False
    
    class MockDevice:
        def __init__(self, *args, **kwargs): 
            self._distance = 2.0
        @property
        def distance(self): return self._distance
        @property
        def is_pressed(self): return False
        @property
        def value(self): return 0
        @value.setter
        def value(self, v): pass
        def beep(self, *args, **kwargs): print("!!! BEEP !!!")
        def on(self): pass
        def off(self): pass
        def play(self, *args, **kwargs): print("!!! PLAY TONE !!!")
        def stop(self): print("!!! STOP TONE !!!")
    
    DigitalOutputDevice = MockDevice
    Button = MockDevice
    DistanceSensor = MockDevice
    TonalBuzzer = MockDevice

# Initialize OLED Display
display = DisplayManager()

# Initialize FaceRecognizer
people = program.get_authorized_people()
recognizer = program.FaceRecognizer(people)

# Pin Configuration
MOTOR_PINS = [14, 15, 18, 23]
BTN_CLOSE_PIN = 16
ULTRASONIC_TRIG = 27
ULTRASONIC_ECHO = 17
BUZZER_PIN = 22

# Initialize Hardware
stepper_obj = []
for gpio in MOTOR_PINS:
    stepper_obj.append(DigitalOutputDevice(gpio))

btn_close_lock = Button(BTN_CLOSE_PIN, pull_up=True)

try:
    ultrasonic = DistanceSensor(echo=ULTRASONIC_ECHO, trigger=ULTRASONIC_TRIG, max_distance=2.0)
except Exception as e:
    print(f"WARNING: Ultrasonic sensor failed to initialize: {e}")
    class MockSensor:
        def __init__(self): self.distance = 2.0
    ultrasonic = MockSensor()

buzzer = TonalBuzzer(BUZZER_PIN)

lock_closed = True
seq_pointer = [0, 1, 2, 3, 4, 5, 6, 7]
current_speed = 0

arrSeq = [[0,0,0,1],
          [0,0,1,1],
          [0,0,1,0],
          [0,1,1,0],
          [0,1,0,0],
          [1,1,0,0],
          [1,0,0,0],
          [1,0,0,1]]

def get_current_speed():
    global current_speed
    if lock_closed:
        current_speed = 0
    else:
        current_speed = max(0, min(45, current_speed + random.randint(-2, 3)))
    return current_speed

def angle_to_position(angle):
    angle = int(angle)
    if angle < 0:
        position = int(4100/360 * angle * -1)
        direction = -1
    elif angle > 0:
        position = int(4100/360 * angle)
        direction = 1
    else:
        position = 0
        direction = 0
    return [position, direction]

def stepper_move(direction, speed, position):
    global seq_pointer
    position_counter = 0
    while position_counter < position:
        seq_pointer = seq_pointer[direction:] + seq_pointer[:direction]
        for i in range(len(stepper_obj)):
            stepper_obj[i].value = arrSeq[seq_pointer[0]][i]
        sleep(0.005/speed)
        position_counter += 1

print("\n--- Smart Bike System Ready ---")
display.show_locked()

while True:
    try:
        # --- 1. PROXIMITY & DASHBOARD (Only Active When Unlocked) ---
        if not lock_closed:
            try:
                dist = ultrasonic.distance * 100
            except Exception:
                dist = 200.0
                
            warning_msg = None
            if dist < 30:
                warning_msg = "CLOSE OBJECT"
                buzzer.play(880)
            else:
                buzzer.stop()

            speed = get_current_speed()
            display.show_dashboard(speed, warning=warning_msg)
        else:
            # Ensure buzzer is off when locked
            buzzer.stop()

        # --- 2. LOCK CONTROL LOGIC ---
        
        # CLOSE LOCK: Press button while open
        if btn_close_lock.is_pressed and not lock_closed:
            print("Closing lock...")
            display.show_closing()
            result = angle_to_position(-90)
            stepper_move(result[1], 5, result[0])
            lock_closed = True
            print("Lock CLOSED.")
            display.show_locked()

        # OPEN LOCK: Start facial recognition while closed
        if lock_closed:
            if program.main(recognizer):
                name = recognizer.last_detected_name or "User"
                print(f"Face recognized: {name}! Opening lock...")
                display.show_welcome(name)
                
                result = angle_to_position(90)
                stepper_move(result[1], 5, result[0])
                lock_closed = False
                print("Lock OPEN.")
                sleep(2)
            else:
                # Small delay if no face was found or system was idle
                sleep(1)
        
        sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping Smart Bike...")
        display.clear()
        break
    except Exception as e:
        print(f"Error in main loop: {e}")
        sleep(2)
