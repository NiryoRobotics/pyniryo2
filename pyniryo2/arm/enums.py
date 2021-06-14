from enum import Enum, unique

@unique
class CalibrateMode(Enum):
    """
    Enumeration of Calibration Modes
    """
    AUTO = 1
    MANUAL = 2


@unique
class RobotAxis(Enum):
    """
    Enumeration of Robot Axis : it used for Shift command
    """
    X = 0
    Y = 1
    Z = 2
    ROLL = 3
    PITCH = 4
    YAW = 5

@unique
class JogShift(Enum):
    """
    Enumeration of Jog Shift : it used for Jog commands
    """
    JOINTS_SHIFT = 1
    POSE_SHIFT = 2


@unique
class ArmMoveCommandType(Enum):
    """
    Enumeration of Arm Move Command : it used for move commands
    """
    JOINTS = 0  # uses joints
    POSE = 1  # uses position and rpy
    POSITION = 2  # uses position
    RPY = 3  # uses rpy
    POSE_QUAT = 4  # uses position and orientation
    LINEAR_POSE = 5  # uses position and rpy
    SHIFT_POSE = 6  # uses shift
    SHIFT_LINEAR_POSE = 7  # uses shift
    EXECUTE_TRAJ = 8  # uses dist_smoothing, list_poses
    DRAW_SPIRAL = 9
