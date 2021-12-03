from enum import Enum, unique


@unique
class ManageTrajectories(Enum):
    """
    Enumeration of actions available for saved trajectories management
    """
    DELETE = -1
    SAVE = 1
