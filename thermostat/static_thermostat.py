from thermostat.thermostat import Thermostat

class StaticThermostat(Thermostat):
    def __init__(self, hardware, threshold, target_temperature):
        super().__init__(hardware, threshold)
        self.target_temperature = target_temperature

    def run(self):
        hw_status = self.hardware.get_status()
        self.toggle_hardware(hw_status["temperature"], self.target_temperature)
        result = {
            "type": "static",
            "target_temperature": self.target_temperature,
            "threshold": self.threshold,
            "hardware_status": hw_status
        }
        return result

