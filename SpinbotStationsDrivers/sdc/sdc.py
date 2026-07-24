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

    def test(self):
        self.pump.draw_and_dispense(
            draw_valve_port=1,
            dispense_valve_port=2,
            volume=1,
        )