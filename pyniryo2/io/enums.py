from enum import Enum, unique


@unique
class PinMode(Enum):
    """
    Enumeration of Pin Modes
    """
    INPUT = 0
    OUTPUT = 1


@unique
class PinState(Enum):
    """
    Pin State is either LOW or HIGH
    """
    LOW = 0
    HIGH = 1


@unique
class PinID(Enum):
    """
    Enumeration of Robot Pins
    """
    GPIO_1A = 0
    GPIO_1B = 1
    GPIO_1C = 2
    GPIO_2A = 3
    GPIO_2B = 4
    GPIO_2C = 5
