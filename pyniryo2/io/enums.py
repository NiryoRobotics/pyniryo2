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
    GPIO_1A = "1A"
    GPIO_1B = "1B"
    GPIO_1C = "1C"
    GPIO_2A = "2A"
    GPIO_2B = "2B"
    GPIO_2C = "2C"

    SW_1 = "SW1"
    SW_2 = "SW2"

    DO1 = "DO1"
    DO2 = "DO2"
    DO3 = "DO3"
    DO4 = "DO4"
    DI1 = "DI1"
    DI2 = "DI2"
    DI3 = "DI3"
    DI4 = "DI4"
    DI5 = "DI5"
