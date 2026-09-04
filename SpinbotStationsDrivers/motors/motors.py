from time import sleep
from gpiozero import DigitalOutputDevice

ENABLED = 0
DISABLED = 1

class MultiMotorController:
    def __init__(self, step_pin, direction_pin, enable_pins, step_delay=0.001, switch_delay=0.01):
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
        self.motors_count = len(self.enables)

        self.positions = [0] * self.motors_count
        self._active_motor = None
        return

    # --------------------------INTERNAL--------------------------



    # ---------------------------PUBLIC---------------------------
    
    def disable_all(self):
        """Sets the enable pin high (turning off driver) for all drivers
        """
        for en in self.enables:
            en.value = DISABLED
        self._active_motor = None
        return

    def select(self, motor_index:int):
        """Select the index of the current motor to work with 

        Args:
            motor_index (int): index of motor in enable_pins
        """

        # check to see if index is possible
        if not (0 <= motor_index < self.motors_count):
            raise ValueError(f"Tried to access a motor using an index that does not exsist."
                             f"\nIndex motor {motor_index}. Value should be between 0 and {motor_count}")
        if motor_index == self._active_motor:
            return
        
        self.disable_all()      # turn off all motors
        self.enables[motor_index].value = ENABLED
        self._active_motor = motor_index
        if self.switch_delay:
            sleep(self.switch_delay)
        return
    