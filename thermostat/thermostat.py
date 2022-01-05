class Thermostat():
    def __init__(self, hardware, threshold):
        self.hardware = hardware
        self.threshold = threshold

    def run(self):
        pass

    def turn_off(self):
        self.hardware.turn_off()

    def toggle_hardware(self, temperature, target):
        if(temperature > target + self.threshold):
            self.hardware.toggle_heater(False)
            self.hardware.toggle_cooler(True)
        elif(temperature < target - self.threshold):
            self.hardware.toggle_heater(True)
            self.hardware.toggle_cooler(False)
        else:
            # initialize smart mode
            self.hardware.toggle_heater(False)
            self.hardware.toggle_cooler(False)