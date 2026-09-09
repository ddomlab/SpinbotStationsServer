from time import sleep
from gpiozero import OutputDevice



if False:
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
else:
    from SpinbotStationsDrivers import motors
    steppers = motors.MultiStepperController(
        step_pin=21,
        direction_pin=20,
        enable_pins=[13, 19, 26],
        step_delay=0.001,
        switch_delay=0.01
    )

    for _ in range(0, 10):
        for index in range(0, steppers.num_motors):
            steppers.step_motor(index, 600, True)
