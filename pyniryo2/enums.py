from enum import Enum, unique

@unique
class RobotErrors(Enum):
    
    # overall behavior
    SUCCESS = 1
    CANCELLED = 2
    PREEMPTED = 3

    FAILURE = -1
    ABORTED = -3
    STOPPED = -4

    ROS_ERROR = -20

    FILE_ALREADY_EXISTS = -30

    UNKNOWN_COMMAND = -50
    NOT_IMPLEMENTED_COMMAND = -51
    INVALID_PARAMETERS = -52

    # - Hardware
    HARDWARE_FAILURE = -110
    HARDWARE_NOT_OK = -111
    LEARNING_MODE_ON = -112
    CALIBRATION_NOT_DONE = -113
    DIGITAL_IO_PANEL_ERROR = -114
    LED_MANAGER_ERROR = -115
    BUTTON_ERROR = -116
    WRONG_MOTOR_TYPE = -117
    DXL_WRITE_ERROR = -118
    DXL_READ_ERROR = -119
    CAN_WRITE_ERROR = -120
    CAN_READ_ERROR = -121
    NO_CONVEYOR_LEFT = -122
    NO_CONVEYOR_FOUND = -123
    CONVEYOR_ID_INVALID = -124
    CALIBRATION_IN_PROGRESS = -125

    # - Vision
    VIDEO_STREAM_ON_OFF_FAILURE = -170
    VIDEO_STREAM_NOT_RUNNING = -171
    OBJECT_NOT_FOUND = -172
    MARKERS_NOT_FOUND = -173

    # - Commander
    # Arm Commander
    ARM_COMMANDER_FAILURE = -220
    GOAL_STILL_ACTIVE = -221
    JOG_CONTROLLER_ENABLED = -222
    CONTROLLER_PROBLEMS = -223
    SHOULD_RESTART = -224
    JOG_CONTROLLER_FAILURE = -225

    PLAN_FAILED = -230
    NO_PLAN_AVAILABLE = -231
    INVERT_KINEMATICS_FAILURE = -232

    # Tool Commander
    TOOL_FAILURE = -251
    TOOL_ID_INVALID = -252
    TOOL_NOT_CONNECTED = -253
    TOOL_ROS_INTERFACE_ERROR = -254

    # - Pose Handlers
    POSES_HANDLER_CREATION_FAILED = -300
    POSES_HANDLER_REMOVAL_FAILED = -301
    POSES_HANDLER_READ_FAILURE = -302
    POSES_HANDLER_COMPUTE_FAILURE = -303

    WORKSPACE_CREATION_FAILED = -308

    # - Programs Manager
    PROGRAMS_MANAGER_FAILURE = -320
    PROGRAMS_MANAGER_READ_FAILURE = -321
    PROGRAMS_MANAGER_UNKNOWN_LANGUAGE = -325
    PROGRAMS_MANAGER_NOT_RUNNABLE_LANGUAGE = -326
    PROGRAMS_MANAGER_EXECUTION_FAILED = -327
    PROGRAMS_MANAGER_STOPPING_FAILED = -328
    PROGRAMS_MANAGER_AUTORUN_FAILURE = -329
    PROGRAMS_MANAGER_WRITING_FAILURE = -330
    PROGRAMS_MANAGER_FILE_ALREADY_EXISTS = -331
    PROGRAMS_MANAGER_FILE_DOES_NOT_EXIST = -332


    # - Serial
    SERIAL_FILE_ERROR = -400
    SERIAL_UNKNOWN_ERROR = -401

    # - MQTT Client
    MQTT_PUBLISH_FUNCTION_DOESNT_EXIST = -420
    MQTT_PUBLISH_FUNCTION_INVALID_ARGUMENTS = -421

    # - System Api Client
    SYSTEM_API_CLIENT_UNKNOWN_ERROR = -440
    SYSTEM_API_CLIENT_INVALID_ROBOT_NAME = -441
    SYSTEM_API_CLIENT_REQUEST_FAILED = -442

@unique
class ArmMoveCommandType(Enum):
    """
    Enumeration of Arm Move Command : it used for move commands
    """
    JOINTS = 0            # uses joints 
    POSE = 1              # uses position and rpy 
    POSITION = 2          # uses position
    RPY = 3               # uses rpy
    POSE_QUAT = 4         # uses position and orientation
    LINEAR_POSE = 5       # uses position and rpy
    SHIFT_POSE = 6        # uses shift
    SHIFT_LINEAR_POSE = 7 # uses shift
    EXECUTE_TRAJ = 8      # uses dist_smoothing, list_poses
    DRAW_SPIRAL = 9
    DRAW_CIRCLE = 10
    EXECUTE_FULL_TRAJ = 11
    EXECUTE_RAW_TRAJ = 12
