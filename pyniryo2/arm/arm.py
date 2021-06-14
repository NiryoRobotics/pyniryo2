# - Imports
from __future__ import print_function

# Python libraries
import roslibpy
import time

# Communication imports
from pyniryo2.robot_commander import RobotCommander
from pyniryo2.arm.enums import CalibrateMode, RobotAxis, JogShift
from pyniryo2.enums import RobotErrors
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
        def wait_calibration_end():
            calibration_finished = False
            while not calibration_finished:
                time.sleep(0.05)
                hardware_status = self._topics.hardware_status_topic()
                if hardware_status:
                    calibration_finished = not(hardware_status["calibration_in_progress"] or hardware_status["calibration_needed"])

        self._check_enum_belonging(calibrate_mode, CalibrateMode)
        request = roslibpy.ServiceRequest()
        request["value"] = calibrate_mode.value

        if callback is not None:
            self._services.request_calibration_service.call(request, callback=callback, errback=errback,
                                                            timeout=timeout)
        else:
            resp = self._services.request_calibration_service.call(request, callback=None, errback=errback,
                                                            timeout=timeout)
            wait_calibration_end()
            return resp["status"] >= RobotErrors.SUCCESS.value


    def calibrate_auto(self, callback=None, errback=None, timeout=None):
        """
        Start a automatic motors calibration if motors are not calibrated yet

        :rtype: None
        """
        return self.calibrate(CalibrateMode.AUTO, callback, errback, timeout)

    def request_new_calibration(self, callback=None, errback=None, timeout=None):
        """
        Start a automatic motors calibration even if motors are calibrated yet

        :rtype: None
        """
        self.reset_calibration()
        return self.calibrate_auto(callback, errback, timeout)

    def reset_calibration(self):
        request = self._services.get_trigger_request()
        self._services.request_new_calibration_service.call(request)

        hardware_status = self._topics.hardware_status_topic()
        while not hardware_status or not hardware_status["calibration_needed"]:
            hardware_status = self._topics.hardware_status_topic()
            time.sleep(0.05)

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
        return self._topics.learning_mode_state_topic()['data']

    @learning_mode.setter
    def learning_mode(self, value):
        self.set_learning_mode(value)

    def set_learning_mode(self, enabled):
        """
        Set learning mode if param is ``True``, else turn it off

        :param enabled: ``True`` or ``False``
        :type enabled: bool
        :rtype: None
        """
        self._check_type(enabled, bool)
        req = self._services.get_learning_mode_request(enabled)
        resp = self._services.activate_learning_mode_service.call(req)
        return resp["status"] >= RobotErrors.SUCCESS.value


    # - Get Joints/Pose

    @property
    def joints_state(self):
        """
        Get the joints state topic.
        The message returned by the topic is formalized in the following form:
        dict{"header": dict{"seq": uint32, "stamp": time, "frame_id": string},
             "position": list[float],
             "velocity": list[float],
             "effort": list[float] }

        It can be used as follows:: ::

            # Get last joint state
            arm.joints_state()
            amr.joints_state.value

            # Raise a callback at each new value
            from __future__ import print_function

            arm.joints_state.subscribe(lambda message: print(message['position']))
            arm.joints_state.unsubscribe()


        :return: Joint states topic.
        :rtype: NiryoTopic
        """
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

    def move_to_home_pose(self):
        """
        Move to a position where the forearm lays on shoulder

        :rtype: None
        """
        self.move_joints(0.0, 0.3, -1.3, 0.0, 0.0, 0.0)

    def go_to_sleep(self):
        """
        Go to home pose and activate learning mode

        :rtype: None
        """
        self.move_to_home_pose()
        self.set_learning_mode(True)

    def move_linear_pose(self, *args):
        """
        Move robot end effector pose to a (x, y, z, roll, pitch, yaw) pose in a linear way

        :param args: either 6 args (1 for each coordinates) or a list of 6 coordinates or a PoseObject
        :type args: Union[tuple[float], list[float], PoseObject]
        :rtype: None
        """
        pose_list = self.__args_pose_to_list(*args)
        goal = self._actions.get_move_linear_pose_goal(pose_list)
        goal.send(result_callback=None)
        _result = goal.wait(self.__action_timeout)

    def stop_move(self, callback=None, errback=None, timeout=None):
        self._services.stop_arm_service.call(self._services.get_trigger_request(), callback, errback, timeout)

    @property
    def get_arm_max_velocity(self):
        """
        Get current arm max velocity by a percentage of its maximum velocity

        :return:
        :rtype:
        """
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

    def shift_pose(self, axis, shift_value):
        """
        Shift robot end effector pose along one axis

        :param axis: Axis along which the robot is shifted
        :type axis: RobotAxis
        :param shift_value: In meter for X/Y/Z and radians for roll/pitch/yaw
        :type shift_value: float
        :rtype: None
        """
        self._check_enum_belonging(axis, RobotAxis)
        shift_value = self._transform_to_type(shift_value, float)

        goal = self._actions.get_shift_pose_goal(axis, shift_value)
        goal.send()
        _result = goal.wait(self.__action_timeout)

    # - Jog

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

    def jog_joints(self, *args):
        """
        Jog robot joints'.
        Jog corresponds to a shift without motion planning.
        Values are expressed in radians.

        :param args: either 6 args (1 for each joints) or a list of 6 joints offset
        :type args: Union[list[float], tuple[float]]
        :rtype: None
        """
        joints_offset = self.__args_joints_to_list(*args)
        req = self._services.get_jog_request(JogShift.JOINTS_SHIFT.value, joints_offset)
        self._services.jog_shift_service.call(req)#, callback, errback, timeout)

    def jog_pose(self, *args):
        """
        Jog robot end effector pose
        Jog corresponds to a shift without motion planning
        Arguments are [dx, dy, dz, d_roll, d_pitch, d_yaw]
        dx, dy & dz are expressed in meters / d_roll, d_pitch & d_yaw are expressed in radians

        :param args: either 6 args (1 for each coordinates) or a list of 6 offset
        :type args: Union[list[float], tuple[float]]
        :rtype: None
        """
        pose_offset = self.__args_joints_to_list(*args)
        req = self._services.get_jog_request(JogShift.POSE_SHIFT.value, pose_offset)
        self._services.jog_shift_service.call(req)  # , callback, errback, timeout)

    # -- Kinematics

    def forward_kinematics(self, *args):
        """
        Compute forward kinematics of a given joints configuration and give the
        associated spatial pose

        :param args: either 6 args (1 for each joints) or a list of 6 joints
        :type args: Union[list[float], tuple[float]]
        :rtype: PoseObject
        """
        joints = self.__args_joints_to_list(*args)
        request = self._services.get_forward_kinematics_request(joints)
        response = self._services.forward_kinematics_service.call(request)

        pose_array = self.__args_pose_to_list(response["pose"])
        pose_object = PoseObject(*pose_array)
        return pose_object

    def inverse_kinematics(self, *args):
        """
        Compute inverse kinematics

        :param args: either 6 args (1 for each coordinates) or a list of 6 coordinates or a ``PoseObject``
        :type args: Union[tuple[float], list[float], PoseObject]

        :return: List of joints value
        :rtype: list[float]
        """
        pose_list = self.__args_pose_to_list(*args)
        request = self._services.get_inverse_kinematics_request(pose_list)
        response = self._services.inverse_kinematics_service.call(request)
        return response["joints"]

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
