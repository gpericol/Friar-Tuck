from hardware.abstract_hardware import *
from data.config.config import *
import RPi.GPIO as GPIO
import os

class RealHardware(AbstractHardware):
    def __init__(self):
        # Relay
        self.in_heater = CONFIG["in_heater"]
        self.in_cooler = CONFIG["in_cooler"]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.in_heater, GPIO.OUT)
        GPIO.setup(self.in_cooler, GPIO.OUT)
        GPIO.output(self.in_heater,False)
        GPIO.output(self.in_cooler,False)
        self.heater = False
        self.cooler = False

        # Thermo
        self.sensor_path = None
        os.system('sudo modprobe w1-gpio')
        os.system('sudo modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices'

        dir_list = os.listdir(base_dir)

        for path in dir_list:
            if path.startswith("28"):
                self.sensor_path = os.path.join(base_dir, path, "w1_slave")

        if self.sensor_path == None:
            raise HardwareError("No thermo sensor")
        
        self.temperature = 0

    def get_status(self):
        self._get_temperature()
        return {
            "temperature": self.temperature,
            "heater": self.heater,
            "cooler": self.cooler
        }

    def _get_temperature(self):
        with open(self.sensor_path, 'r') as sensor_file:
            self.temperature = round(int(sensor_file.readlines()[1].split("=")[1]) / 1000, 1)
            

    def toggle_heater(self, turned_on):
        GPIO.output(self.in_heater,turned_on)
        self.heater = turned_on


    def toggle_cooler(self, turned_on):
        GPIO.output(self.in_cooler,turned_on)
        self.cooler = turned_on

    def turn_off(self):
        GPIO.cleanup()
