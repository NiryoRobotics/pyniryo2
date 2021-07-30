from enum import Enum, unique


@unique
class AnimationMode(Enum):
    """
    Enumeration of animations available for the user to control the Led Ring
    """
    NONE = -1
    SOLID = 1
    FLASHING = 2    
    ALTERNATE = 3   
    CHASE = 4       
    COLOR_WIPE = 5  
    RAINBOW = 6
    RAINBOW_CYLE = 7
    RAINBOW_CHASE = 8
    GO_UP = 9
    GO_UP_AND_DOWN = 10