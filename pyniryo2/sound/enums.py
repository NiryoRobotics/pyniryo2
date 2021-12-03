from enum import Enum, unique


@unique
class SoundNameID(Enum):
    """
    Enumeration of the different SoundName Ids
    """
    SOUND_ALARM=1
    SOUND_WARNING=2
    SOUND_ON=3
    SOUND_OFF=4
    SOUND_LM_ON=5
    SOUND_LM_OFF=6
