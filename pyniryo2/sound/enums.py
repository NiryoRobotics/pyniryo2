from enum import Enum, unique


@unique
class ManageSound(Enum):
    """
    Enumeration of the actions of sound database management
    """
    ADD = 1
    DELETE = 2
