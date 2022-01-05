from hardware.abstract_hardware import *
import random

class FakeHardware(AbstractHardware):
    def __init__(self):
        self.temperature = 0
        self.heater = False
        self.cooler = False
    
    def get_status(self):
        value = random.random()
        if self.heater:
            self.temperature += value
        elif self.cooler:
            self.temperature -= value 
        else:
            self.temperature += (-round(random.random())) + value 

        self.temperature = round(self.temperature, 1)
        return {
            "temperature": self.temperature,
            "heater": self.heater,
            "cooler": self.cooler
        }

    def toggle_heater(self, turned_on):
        self.heater = turned_on

    def toggle_cooler(self, turned_on):
        self.cooler = turned_on

    def turn_off(self):
        self.temperature = 0
        self.heater = False
        self.cooler = False
