# - Imports
from __future__ import print_function

# Python libraries
import roslibpy
import time

# Communication imports
from pyniryo2.robot_commander import RobotCommander
from pyniryo2.arm.enums import CalibrateMode, RobotAxis
from pyniryo2.objects import PoseObject

from pyniryo2.arm.services import ArmServices
from pyniryo2.arm.topics import ArmTopics
from pyniryo2.arm.actions import ArmActions

class Arm(RobotCommander):
    # --- Public functions --- #
    def __init__(self, client):
        super(Arm, self).__init__(client)

        self._services = ArmServices(self._client)
        self._topics = ArmTopics(self._client)
        self._actions = ArmActions(self._client)

        self.__action_timeout = 10

    # - Main purpose

    # -- Calibration

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
        self._services.request_calibration_service.call(request, callback, errback, timeout)
        time.sleep(0.5)

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
        self._services.request_new_calibration_service.call(request, callback, errback, timeout)

        if not callback:
            calibrate()

    def need_calibration(self):
        """
        Return a bool indicating whereas the robot motors need to be calibrate

        :rtype: bool
        """
        hardware_status = self._topics.hardware_status_topic()
        return hardware_status["calibration_needed"]

    # - Hardware Status

    @property
    def hardware_status(self):
        return self._topics.hardware_status_topic

    # -- Learning mode

    @property
    def learning_mode(self):
        return self._topics.learning_mode_state_topic

    def get_learning_mode(self):
        """
        Get learning mode state

        :return: ``True`` if learning mode is on
        :rtype: bool
        """
        return self._topics.learning_mode_state_topic()

    @learning_mode.setter
    def learning_mode(self, value):
        self.set_learning_mode(value)

    def set_learning_mode(self, enabled,  callback=None, errback=None, timeout=None):
        """
        Set learning mode if param is ``True``, else turn it off

        :param enabled: ``True`` or ``False``
        :type enabled: bool
        :rtype: None
        """
        self._check_type(enabled, bool)
        req = self._services.get_learning_mode_request(enabled)
        self._services.activate_learning_mode_service.call(req, callback, errback, timeout)


    def set_jog_control(self, enabled,  callback, errback, timeout):
        """
        Set jog control mode if param is True, else turn it off

        :param enabled: ``True`` or ``False``
        :type enabled: bool
        :rtype: None
        """
        self._check_type(enabled, bool)
        req = self._services.get_enable_jog_request(enabled)
        self._services.enable_jog_controller_service.call(req, callback, errback, timeout)


    # - Get Joints/Pose

    @property
    def joints_state(self):
        return self._topics.joint_states_topic

    @property
    def joints(self):
        return self.get_joints()

    def get_joints(self):
        """
        Get joints value in radians
        You can also use a getter ::

            joints = robot.get_joints()
            joints = robot.joints

        :return: List of joints value
        :rtype: list[float]
        """
        return self._topics.joint_states_topic()["position"]

    @property
    def robot_pose(self):
        """

        See below some usage ::

            arm.robot_pose()
            arm.robot_pose.subscribe(callback)
            arm.robot_pose.unsubscribe()
            arm.robot_pose.value

        :return:
        :rtype:
        """
        return self._topics.robot_state_topic

    @property
    def pose(self):
        return self.get_pose()

    def get_pose(self):
        """
        Get end effector link pose as [x, y, z, roll, pitch, yaw].
        x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians
        You can also use a getter ::

            pose = robot.get_pose()
            pose = robot.pose

        :rtype: PoseObject
        """
        robot_state = self._topics.robot_state_topic()
        x, y, z = robot_state["position"]["x"], robot_state["position"]["y"], robot_state["position"]["z"]
        roll, pitch, yaw = robot_state["rpy"]["roll"], robot_state["rpy"]["pitch"], robot_state["rpy"]["yaw"]
        pose_object = PoseObject(x, y, z, roll, pitch, yaw)
        return pose_object

    def get_pose_quat(self):
        """
        Get end effector link pose in Quaternion coordinates

        :return: Position and quaternion coordinates concatenated in a list : [x, y, z, qx, qy, qz, qw]
        :rtype: list[float]
        """
        robot_state = self._topics.robot_state_topic()
        x, y, z = robot_state["position"]["x"], robot_state["position"]["y"], robot_state["position"]["z"]
        qx, qy, qz, qw = robot_state["orientation"]["x"], robot_state["orientation"]["y"], robot_state["orientation"]["z"], robot_state["orientation"]["w"]
        return [x, y, z, qx, qy, qz, qw]

    # --  Simple Move

    @joints.setter
    def joints(self, *args):
        self.move_joints(*args)

    def move_joints(self, *args):
        """
        Move robot joints. Joints are expressed in radians.

        All lines of the next example realize the same operation: ::

            robot.joints = [0.2, 0.1, 0.3, 0.0, 0.5, 0.0]
            robot.move_joints([0.2, 0.1, 0.3, 0.0, 0.5, 0.0])
            robot.move_joints(0.2, 0.1, 0.3, 0.0, 0.5, 0.0)

        :param args: either 6 args (1 for each joints) or a list of 6 joints
        :type args: Union[list[float], tuple[float]]
        :rtype: None
        """
        joints = self.__args_joints_to_list(*args)
        goal = self._actions.get_move_joints_goal(joints)
        goal.send()
        _result = goal.wait(self.__action_timeout)


    @pose.setter
    def pose(self, *args):
        self.move_pose(*args)

    def move_pose(self, *args):
        """
        Move robot end effector pose to a (x, y, z, roll, pitch, yaw) pose.
        x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians

        All lines of the next example realize the same operation: ::

            robot.pose = [0.2, 0.1, 0.3, 0.0, 0.5, 0.0]
            robot.move_pose([0.2, 0.1, 0.3, 0.0, 0.5, 0.0])
            robot.move_pose(0.2, 0.1, 0.3, 0.0, 0.5, 0.0)
            robot.move_pose(PoseObject(0.2, 0.1, 0.3, 0.0, 0.5, 0.0))

        :param args: either 6 args (1 for each coordinates) or a list of 6 coordinates or a ``PoseObject``
        :type args: Union[tuple[float], list[float], PoseObject]

        :rtype: None
        """
        pose_list = self.__args_pose_to_list(*args)
        goal = self._actions.get_move_pose_goal(pose_list)
        goal.send(result_callback=None)
        _result = goal.wait(self.__action_timeout)

    @property
    def arm_max_velocity(self):
        return self._topics.max_velocity_scaling_factor_topic

    def set_arm_max_velocity(self, percentage_speed, callback=None, errback=None, timeout=None):
        """
        Limit arm max velocity to a percentage of its maximum velocity

        :param percentage_speed: Should be between 1 & 100
        :type percentage_speed: int
        :rtype: None
        """
        self._check_range_belonging(percentage_speed, 1, 100)
        req = self._services.get_max_velocity_scaling_factor_request(percentage_speed)
        self._services.set_max_velocity_scaling_factor_service.call(req, callback, errback, timeout)

    # - Shift Pose

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
    #     self._check_enum_belonging(axis, RobotAxis)
    #     shift_value = self._transform_to_type(shift_value, float)
    #
    #     #self._actions.
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

    # -- Useful functions
    def __args_pose_to_list(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, PoseObject):
                return arg.to_list()
            else:
                pose_list = arg
        else:
            pose_list = args

        pose_list_float = self._map_list(pose_list, float)
        if len(pose_list_float) != 6:
            self._raise_exception("A pose should contain 6 elements (x, y, z, roll, pitch, yaw)")
        return pose_list_float

    def __args_joints_to_list(self, *args):
        """
        Convert args into a list
        Either if args = (1.1,5.6,-6.7) or args = ([1.1,5.6,-6.7],) , the
        function will return (1.1,5.6,-6.7)

        :param args: Union[list, tuple]
        :return: list of float
        """
        if len(args) == 1:
            args = args[0]

        joints = self._map_list(args, float)
        if len(joints) != 6:
            self._raise_exception("The robot has 6 joints")

        return joints
