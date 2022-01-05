from thermostat.thermostat import Thermostat
import time

class SmartThermostat(Thermostat):    
    def __init__(self, hardware, threshold, curve, delay_hours=0):
        super().__init__(hardware, threshold)
        self.curve = curve
        self.start_time = None
        self.smart_mode = False
        self.delay_hours = delay_hours

    def run(self):
        hw_status = self.hardware.get_status()
        # check if we're on target for starting curve
        if (hw_status["temperature"] > self.curve.get_start_temperature() - self.threshold and 
            hw_status["temperature"] < self.curve.get_start_temperature() + self.threshold):
            self.start_time = round(time.time()) - self.delay_hours * 3600
            self.smart_mode = True

        result = {
            "type": "smart",
            "curve_name": self.curve.get_name(),
            "smart_mode": self.smart_mode,
            "threshold": self.threshold,
            "hardware_status": hw_status
        }

        if self.smart_mode == False:
            self.mode_init(hw_status)
            result["running_time"] = 0
        else:
            self.mode_smart(hw_status)
            result["running_time"] = round((time.time() - self.start_time) / 3600)

        return result

    def mode_init(self, hw_status):
        self.toggle_hardware(hw_status["temperature"], self.curve.get_start_temperature())
    
    def mode_smart(self, hw_status):
        target_temperature = self.curve.calculate_temperature(self.start_time, round(time.time()))
        self.toggle_hardware(hw_status["temperature"], target_temperature)
