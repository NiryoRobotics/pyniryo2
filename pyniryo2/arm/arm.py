# - Imports
from __future__ import print_function

# Python libraries
import roslibpy

# Communication imports
from pyniryo2.robot_commander import RobotCommander
from pyniryo2.arm.services import ArmServices
from pyniryo2.arm.topics import ArmTopics
from pyniryo2.arm.enums import CalibrateMode, RobotAxis

class Arm(RobotCommander):
    # --- Public functions --- #
    def __init__(self, client):
        super(Arm, self).__init__(client)

        self.__services = ArmServices(self._client)
        self.__topics = ArmTopics(self._client)

    # - Main purpose
    def calibrate(self, calibrate_mode, callback=None, errback=None, timeout=None):
        """
        Calibrate (manually or automatically) motors. Automatic calibration will do nothing
        if motors are already calibrated

        :param calibrate_mode: Auto or Manual
        :type calibrate_mode: CalibrateMode
        :rtype: None
        """
        self._check_enum_belonging(calibrate_mode, CalibrateMode)
        request = roslibpy.ServiceRequest()
        request["value"] = calibrate_mode.value
        self.__services.request_calibration_service.call(request, callback=callback, errback=errback, timeout=timeout)

    def calibrate_auto(self, callback=None, errback=None, timeout=None):
        """
        Start a automatic motors calibration if motors are not calibrated yet

        :rtype: None
        """
        self.calibrate(CalibrateMode.AUTO, callback, errback, timeout)

    def request_new_calibration(self, callback=None, errback=None, timeout=None):
        """
        Start a automatic motors calibration even if motors are calibrated yet

        :rtype: None
        """
        def calibrate():
            self.calibrate_auto(callback, errback, timeout)

        request = roslibpy.ServiceRequest()
        self.__services.request_new_calibration_service.call(request, callback=calibrate, errback=errback, timeout=timeout)

        if not callback:
            calibrate()


    def need_calibration(self):
        """
        Return a bool indicating whereas the robot motors need to be calibrate


        :rtype: bool
        """
        hardware_status = self.__topics.hardware_status_topic()
        return hardware_status["calibration_needed"]

    def get_hardware_status(self, callback=None):
        if callback:
            self.__topics.hardware_status_topic()
        hardware_status = self.__topics.hardware_status_topic()
        return hardware_status["calibration_needed"]

    def subscribe_hardware_status(self, callback):
        self.__topics.hardware_status_topic.subscribe(callback)
    #
    # @property
    # def learning_mode(self):
    #     return self.get_learning_mode()
    #
    # def get_learning_mode(self):
    #     """
    #     Get learning mode state
    #
    #     :return: ``True`` if learning mode is on
    #     :rtype: bool
    #     """
    #     return eval(self.__send_n_receive(Command.GET_LEARNING_MODE))
    #
    # @learning_mode.setter
    # def learning_mode(self, value):
    #     self.set_learning_mode(value)
    #
    # def set_learning_mode(self, enabled):
    #     """
    #     Set learning mode if param is ``True``, else turn it off
    #
    #     :param enabled: ``True`` or ``False``
    #     :type enabled: bool
    #     :rtype: None
    #     """
    #     self.__check_type(enabled, bool)
    #     self.__send_n_receive(Command.SET_LEARNING_MODE, enabled)
    #
    # def set_arm_max_velocity(self, percentage_speed):
    #     """
    #     Limit arm max velocity to a percentage of its maximum velocity
    #
    #     :param percentage_speed: Should be between 1 & 100
    #     :type percentage_speed: int
    #     :rtype: None
    #     """
    #     self.__check_range_belonging(percentage_speed, 1, 100)
    #     self.__send_n_receive(Command.SET_ARM_MAX_VELOCITY, percentage_speed)
    #
    # def set_jog_control(self, enabled):
    #     """
    #     Set jog control mode if param is True, else turn it off
    #
    #     :param enabled: ``True`` or ``False``
    #     :type enabled: bool
    #     :rtype: None
    #     """
    #     self.__check_type(enabled, bool)
    #     self.__send_n_receive(Command.SET_JOG_CONTROL, enabled)
    #
    # @staticmethod
    # def wait(duration):
    #     """
    #     Wait for a certain time
    #
    #     :param duration: duration in seconds
    #     :type duration: float
    #     :rtype: None
    #     """
    #     time.sleep(duration)
    #
    # # - Joints/Pose
    #
    # @property
    # def joints(self):
    #     return self.get_joints()
    #
    # def get_joints(self):
    #     """
    #     Get joints value in radians
    #     You can also use a getter ::
    #
    #         joints = robot.get_joints()
    #         joints = robot.joints
    #
    #     :return: List of joints value
    #     :rtype: list[float]
    #     """
    #     return self.__send_n_receive(Command.GET_JOINTS)
    #
    # @property
    # def pose(self):
    #     return self.get_pose()
    #
    # def get_pose(self):
    #     """
    #     Get end effector link pose as [x, y, z, roll, pitch, yaw].
    #     x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians
    #     You can also use a getter ::
    #
    #         pose = robot.get_pose()
    #         pose = robot.pose
    #
    #     :rtype: PoseObject
    #     """
    #     data = self.__send_n_receive(Command.GET_POSE)
    #     pose_array = self.__map_list(data, float)
    #     pose_object = PoseObject(*pose_array)
    #     return pose_object
    #
    # def get_pose_quat(self):
    #     """
    #     Get end effector link pose in Quaternion coordinates
    #
    #     :return: Position and quaternion coordinates concatenated in a list : [x, y, z, qx, qy, qz, qw]
    #     :rtype: list[float]
    #     """
    #     data = self.__send_n_receive(Command.GET_POSE_QUAT)
    #     pose_array = self.__map_list(data, float)
    #     return pose_array
    #
    # @joints.setter
    # def joints(self, *args):
    #     self.move_joints(*args)
    #
    # def move_joints(self, *args):
    #     """
    #     Move robot joints. Joints are expressed in radians.
    #
    #     All lines of the next example realize the same operation: ::
    #
    #         robot.joints = [0.2, 0.1, 0.3, 0.0, 0.5, 0.0]
    #         robot.move_joints([0.2, 0.1, 0.3, 0.0, 0.5, 0.0])
    #         robot.move_joints(0.2, 0.1, 0.3, 0.0, 0.5, 0.0)
    #
    #     :param args: either 6 args (1 for each joints) or a list of 6 joints
    #     :type args: Union[list[float], tuple[float]]
    #     :rtype: None
    #     """
    #     joints = self.__args_joints_to_list(*args)
    #     self.__send_n_receive(Command.MOVE_JOINTS, *joints)
    #
    # @pose.setter
    # def pose(self, *args):
    #     self.move_pose(*args)
    #
    # def move_pose(self, *args):
    #     """
    #     Move robot end effector pose to a (x, y, z, roll, pitch, yaw) pose.
    #     x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians
    #
    #     All lines of the next example realize the same operation: ::
    #
    #         robot.pose = [0.2, 0.1, 0.3, 0.0, 0.5, 0.0]
    #         robot.move_pose([0.2, 0.1, 0.3, 0.0, 0.5, 0.0])
    #         robot.move_pose(0.2, 0.1, 0.3, 0.0, 0.5, 0.0)
    #         robot.move_pose(PoseObject(0.2, 0.1, 0.3, 0.0, 0.5, 0.0))
    #
    #     :param args: either 6 args (1 for each coordinates) or a list of 6 coordinates or a ``PoseObject``
    #     :type args: Union[tuple[float], list[float], PoseObject]
    #
    #     :rtype: None
    #     """
    #     pose_list = self.__args_pose_to_list(*args)
    #     self.__send_n_receive(Command.MOVE_POSE, *pose_list)
    #
    # def shift_pose(self, axis, shift_value):
    #     """
    #     Shift robot end effector pose along one axis
    #
    #     :param axis: Axis along which the robot is shifted
    #     :type axis: RobotAxis
    #     :param shift_value: In meter for X/Y/Z and radians for roll/pitch/yaw
    #     :type shift_value: float
    #     :rtype: None
    #     """
    #     self.__check_enum_belonging(axis, RobotAxis)
    #
    #     shift_value = self.__transform_to_type(shift_value, float)
    #     self.__send_n_receive(Command.SHIFT_POSE, axis, shift_value)
    #
    # def jog_joints(self, *args):
    #     """
    #     Jog robot joints'.
    #     Jog corresponds to a shift without motion planning.
    #     Values are expressed in radians.
    #
    #     :param args: either 6 args (1 for each joints) or a list of 6 joints offset
    #     :type args: Union[list[float], tuple[float]]
    #     :rtype: None
    #     """
    #     joints_offset = self.__args_joints_to_list(*args)
    #     self.__send_n_receive(Command.JOG_JOINTS, *joints_offset)
    #
    # def jog_pose(self, *args):
    #     """
    #     Jog robot end effector pose
    #     Jog corresponds to a shift without motion planning
    #     Arguments are [dx, dy, dz, d_roll, d_pitch, d_yaw]
    #     dx, dy & dz are expressed in meters / d_roll, d_pitch & d_yaw are expressed in radians
    #
    #     :param args: either 6 args (1 for each coordinates) or a list of 6 offset
    #     :type args: Union[list[float], tuple[float]]
    #     :rtype: None
    #     """
    #     pose_offset = self.__args_joints_to_list(*args)
    #     self.__send_n_receive(Command.JOG_POSE, *pose_offset)
    #
    # def move_linear_pose(self, *args):
    #     """
    #     Move robot end effector pose to a (x, y, z, roll, pitch, yaw) pose in a linear way
    #
    #     :param args: either 6 args (1 for each coordinates) or a list of 6 coordinates or a PoseObject
    #     :type args: Union[tuple[float], list[float], PoseObject]
    #     :rtype: None
    #     """
    #     pose_list = self.__args_pose_to_list(*args)
    #     self.__send_n_receive(Command.MOVE_LINEAR_POSE, *pose_list)
    #
    # def move_to_home_pose(self):
    #     """
    #     Move to a position where the forearm lays on shoulder
    #
    #     :rtype: None
    #     """
    #     self.move_joints(0.0, 0.3, -1.3, 0.0, 0.0, 0.0)
    #
    # def go_to_sleep(self):
    #     """
    #     Go to home pose and activate learning mode
    #
    #     :rtype: None
    #     """
    #     self.move_to_home_pose()
    #     self.set_learning_mode(True)
    #
    # def forward_kinematics(self, *args):
    #     """
    #     Compute forward kinematics of a given joints configuration and give the
    #     associated spatial pose
    #
    #     :param args: either 6 args (1 for each joints) or a list of 6 joints
    #     :type args: Union[list[float], tuple[float]]
    #     :rtype: PoseObject
    #     """
    #     joints = self.__args_joints_to_list(*args)
    #     data = self.__send_n_receive(Command.FORWARD_KINEMATICS, *joints)
    #
    #     pose_array = self.__map_list(data, float)
    #     pose_object = PoseObject(*pose_array)
    #     return pose_object
    #
    # def inverse_kinematics(self, *args):
    #     """
    #     Compute inverse kinematics
    #
    #     :param args: either 6 args (1 for each coordinates) or a list of 6 coordinates or a ``PoseObject``
    #     :type args: Union[tuple[float], list[float], PoseObject]
    #
    #     :return: List of joints value
    #     :rtype: list[float]
    #     """
    #     pose_list = self.__args_pose_to_list(*args)
    #
    #     return self.__send_n_receive(Command.INVERSE_KINEMATICS, *pose_list)