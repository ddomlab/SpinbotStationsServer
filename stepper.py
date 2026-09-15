from SpinbotStationsDrivers import motors

steppers = motors.MultiStepperController(
    step_pin=21,
    direction_pin=20,
    enable_pins=[13, 19, 26],
    step_delay=0.001,
    switch_delay=0.01
)

steppers.test_motors()
