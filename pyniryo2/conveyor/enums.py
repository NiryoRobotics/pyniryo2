from enum import Enum, unique

@unique

class ConveyorID(Enum):
    """
    Enumeration of the different Conveyor Ids
    """
    NONE = 0
    ID_1 = 12
    ID_2 = 13

@unique

class ConveyorDirection(Enum):
    """
    Enumeration of the directions of the conveyor
    """

    FORWARD = 1
    BACKWARD = -1

@unique

class ConveyorStatus(Enum):
    """
    Enumeration of the different Conveyor status
    """

    ADD = 1
    REMOVE = 2