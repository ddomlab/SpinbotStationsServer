from SpinbotStationsDrivers import motors
from time import sleep

steppers = motors.MultiStepperController(
    step_pin=21,
    direction_pin=20,
    enable_pins=[13, 19, 26],
    step_delay=0.001,
    switch_delay=0.01
)

steppers.step_out(1, 400)

def action_one():
    steppers.step_counterclockwise(1, 200)

def move(motor_index: int, steps: int):
    """Move a configured motor by a signed number of steps."""
    if steps >= 0:
        steppers.step_clockwise(motor_index, steps)
    else:
        steppers.step_counterclockwise(motor_index, abs(steps))
