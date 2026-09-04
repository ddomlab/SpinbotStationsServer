from time import sleep
from gpiozero import OutputDevice

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 7.5)
delay = .001
step_count = SPR

dir_pin = OutputDevice(DIR)
step_pin = OutputDevice(STEP)

while True:
    var = input("Direction:")
    if var == '1':
        dir_pin.value = CW
        print("Spinning CW")
        for _ in range(step_count):
            step_pin.on()
            sleep(delay)
            step_pin.off()
            sleep(delay)
    elif var == '2':
        dir_pin.value = CCW
        print("Spinning CCW")
        for _ in range(step_count):
            step_pin.on()
            sleep(delay)
            step_pin.off()
            sleep(delay)
        pass
    else:
        dir_pin.close()
        step_pin.close()
        break
