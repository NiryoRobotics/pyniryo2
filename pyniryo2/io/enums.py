from enum import Enum, unique


@unique
class PinMode(Enum):
    """
    Enumeration of Pin Modes
    """
    OUTPUT = 0
    INPUT = 1


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
    GPIO_1A = 2
    GPIO_1B = 3
    GPIO_1C = 16
    GPIO_2A = 26
    GPIO_2B = 19
    GPIO_2C = 6

    SW_1 = 12
    SW_2 = 13
