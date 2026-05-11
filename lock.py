import program
from time import sleep
import os
from display_manager import DisplayManager

# Try to import gpiozero, fallback to a mock if not on a Raspberry Pi
try:
    from gpiozero import DigitalOutputDevice, Button
    # Test if a pin factory is available
    from gpiozero.devices import Device
    Device.ensure_pin_factory()
    HAS_GPIO = True
except (ImportError, Exception):
    print("WARNING: gpiozero could not find a pin factory (Not on a Raspberry Pi?). Using Mock GPIO.")
    HAS_GPIO = False
    class MockDevice:
        def __init__(self, *args, **kwargs): pass
        @property
        def is_pressed(self): return False
        @property
        def value(self): return 0
        @value.setter
        def value(self, v): pass
    DigitalOutputDevice = MockDevice
    Button = MockDevice

# Initialize OLED Display
display = DisplayManager()

# Initialize FaceRecognizer once by automatically finding all JPGs
people = program.get_authorized_people()
recognizer = program.FaceRecognizer(people)

motor_GP = [14,15,18,23]
seq_pointer=[0,1,2,3,4,5,6,7]
stepper_obj = []
btn_close_lock = Button(24, pull_up=True)
lock_closed = True

arrSeq = [[0,0,0,1],
          [0,0,1,1],
          [0,0,1,0],
          [0,1,1,0],
          [0,1,0,0],
          [1,1,0,0],
          [1,0,0,0],
          [1,0,0,1]]



print("Setup pins...")
for gpio in motor_GP:
    stepper_obj.append(DigitalOutputDevice(gpio))



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
    print("DEBUG " + str([position, direction]))
    return [position, direction]

def stepper_move(direction, speed, position):
    global seq_pointer
    position_counter = 0

    while position_counter < position:
        seq_pointer = seq_pointer[direction:] + seq_pointer[:direction]
        print("DEBUG step -> " + str(position_counter))
        for i in range(len(stepper_obj)):
            stepper_obj[i].value = arrSeq[seq_pointer[0]][i]

        sleep(0.005/speed)

        position_counter += 1

print("\n--- Smart Bike Lock Controller Ready ---")
display.show_locked()

while True:
    try:
        # If lock is OPEN, wait for button press to CLOSE it
        if btn_close_lock.is_pressed and not lock_closed:
            print("Closing lock...")
            display.show_closing()
            result = angle_to_position(-90)
            stepper_move(result[1], 5, result[0])
            lock_closed = True
            print("Lock CLOSED.")
            display.show_locked()

        # If lock is CLOSED, start facial recognition to OPEN it
        if lock_closed:
            if program.main(recognizer):
                name = recognizer.last_detected_name or "User"
                print(f"Face recognized: {name}! Opening lock...")
                
                # Show welcome on OLED
                display.show_welcome(name)
                
                result = angle_to_position(90)
                stepper_move(result[1], 5, result[0])
                lock_closed = False
                print("Lock OPEN.")
                
                # Update display to show it's unlocked
                sleep(2)
                display.show_unlocked()
            else:
                # If face recognition failed (e.g. no camera), wait a bit before retrying
                sleep(2)
                display.show_locked()
        else:
            # If lock is open, just wait a bit to avoid high CPU usage
            sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping Smart Bike...")
        display.clear()
        break
    except Exception as e:
        print(f"Error in main loop: {e}")
        sleep(5)
