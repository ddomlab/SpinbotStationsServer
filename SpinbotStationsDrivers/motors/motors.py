from time import sleep
from gpiozero import DigitalOutputDevice

ENABLED = 0
DISABLED = 1

class MultiStepperController:
    def __init__(
            self, 
            step_pin, 
            direction_pin, 
            enable_pins, 
            step_delay=0.001, 
            switch_delay=0.01
            ):
        """This class will be used to drive a number of motors using a motor driver board in conjunction with a custom pihat

        Args:
            step_pin: Pin used to send step commands to selected motor

            direction_pin: Tells motor witch way to spin (CW or CCW)

            enable_pins (array): List of GPIO pins used as the enable pins for motor controllers. Index into this list to select motors (0...N-1)

            step_delay (float, optional): Seconds to hold STEP high and low, per half-pulse. Also sets max step rate. Defaults to 0.001.

            switch_delay (float, optional): Time between switching motor enable pins. Defaults to 0.01.
        """
        self.step_pin_dev = DigitalOutputDevice(step_pin)
        self.dir_pin_dev = DigitalOutputDevice(direction_pin)
        self.step_delay = step_delay
        self.switch_delay = switch_delay

        self.enables = [DigitalOutputDevice(pin) for pin in enable_pins]
        self.num_motors = len(self.enables)

        self.positions = [0] * self.num_motors
        self._active_motor = None

        self.disable_all()
        return

    # --------------------------INTERNAL--------------------------

    

    # ---------------------------PUBLIC---------------------------
    
    def disable_all(self):
        """Sets the enable pin high (turning off driver) for all drivers
        """
        for en in self.enables:
            en.value = DISABLED
            print(f"Motor {en} set to {en.value}")
        self._active_motor = None
        return

    def select(self, motor_index:int):
        """Select the index of the current motor to work with 

        Args:
            motor_index (int): index of motor in enable_pins
        """

        # check to see if index is possible
        if not (0 <= motor_index < self.num_motors):
            raise ValueError(f"Tried to access a motor using an index that does not exsist."
                             f"\nIndex motor {motor_index}. Value should be between 0 and {self.num_motors}")
        if motor_index == self._active_motor:
            return
        
        self.disable_all()      # turn off all motors
        self.enables[motor_index].value = ENABLED
        self._active_motor = motor_index
        if self.switch_delay:
            sleep(self.switch_delay)
        return

    def step_motor(self, motor_index:int, steps:int, clockwise:bool = True):
        self.select(motor_index)
        self.dir_pin_dev.value = clockwise
        direction = 1 if clockwise else -1

        for _ in range(steps):
            self.step_pin_dev.on()
            sleep(self.step_delay)
            self.step_pin_dev.off()
            sleep(self.step_delay)
            self.positions[motor_index] += direction

    def step_clockwise(self, motor_index:int, steps:int):
        self.step_motor(motor_index, steps, True)
        return

    def step_out(self, motor_index:int, steps:int):
        self.step_motor(motor_index, steps, True)
        return

    def step_counterclockwise(self, motor_index:int, steps:int):
        self.step_motor(motor_index, steps, False)
        return

    def step_in(self, motor_index:int, steps:int):
        self.step_motor(motor_index, steps, False)
        return

    def test_motors(self) -> bool:
        for motor in range(0, self.num_motors):
            print(f"Testing motor #{motor}")
            self.step_clockwise(motor, 200)
            self.step_counterclockwise(motor, 200)
        return True
    