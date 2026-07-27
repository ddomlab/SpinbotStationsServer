class sdc:
    def __init__(self):
        from matterlab_pumps import RunzePump
        self.pump = RunzePump(
            com_port='/dev/ttyUSB0',
            address=1,
            syringe_volume=5e-3, # in liters
            num_valve_port=12,
            pump_model='SY01C',
        )

    def run(self, draw_port: int, dispense_port:int, speed:float, volume:float):
        self.pump.draw_and_dispense(
            draw_valve_port=draw_port,
            dispense_valve_port=dispense_port,
            speed=speed,
            volume=volume
        )