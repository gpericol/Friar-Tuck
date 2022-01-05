from abc import ABC, abstractmethod

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class HardwareError(Error):
    def __init__(self, message):
        self.message = message

class AbstractHardware(ABC):
    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def toggle_heater(self, turned_on):
        pass

    @abstractmethod
    def toggle_cooler(self, turned_on):
        pass

    @abstractmethod
    def turn_off(self):
        pass