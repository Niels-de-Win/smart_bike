import program
from time import sleep
from gpiozero import DigitalOutputDevice, Button

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

while True:
    if btn_close_lock.is_pressed and not lock_closed:
        result = angle_to_position(-90)
        stepper_move(result[1], 5, result[0])
        lock_closed = True
    if program.main() and lock_closed:
        result = angle_to_position(90)
        stepper_move(result[1], 5, result[0])
        lock_closed = False
