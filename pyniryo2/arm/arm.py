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
        Calibrates (manually or automatically) motors. Automatic calibration will do nothing
        if motors are already calibrated

        Examples: ::
            # Synchronous use
            arm.calibrate(CalibrateMode.MANUAL)
            arm.calibrate(CalibrateMode.AUTO)

            # Asynchronous use
            def calibration_callback(result):
                if result["status"] < RobotErrors.SUCCESS.value:
                    print("Calibration failed")
                else:
                    print("Calibration completed with success")

            arm.calibrate(CalibrateMode.AUTO, calibration_callback)


        :param calibrate_mode: Auto or Manual
        :type calibrate_mode: CalibrateMode
        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param errback: Callback invoked on error.
        :type errback: function
        :param timeout: Timeout for the operation, in seconds. Only used if blocking.
        :type timeout: float
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """

        def wait_calibration_end():
            for _ in range(40):
                time.sleep(0.05)
                hardware_status = self._topics.hardware_status_topic()
                if hardware_status and not (
                        hardware_status.calibration_in_progress or hardware_status.calibration_needed):
                    return True
            return False

        self._check_enum_belonging(calibrate_mode, CalibrateMode)
        request = roslibpy.ServiceRequest()
        request["value"] = calibrate_mode.value

        if callback is not None:
            self._services.request_calibration_service.call(request, callback=callback, errback=errback,
                                                            timeout=timeout)
            return True
        else:
            resp = self._services.request_calibration_service.call(request, callback=None, errback=errback,
                                                                   timeout=timeout)
            if resp["status"] < RobotErrors.SUCCESS.value:
                return False

            return wait_calibration_end()

    def calibrate_auto(self, callback=None, errback=None, timeout=None):
        """
        Starts a automatic motors calibration if motors are not calibrated yet.

        Examples: ::
            # Synchronous use
            arm.calibrate_auto()

            # Asynchronous use
            def calibration_callback(result):
                if result["status"] < RobotErrors.SUCCESS.value:
                    print("Calibration failed")
                else:
                    print("Calibration completed with success")

            arm.calibrate_auto(calibration_callback)

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param errback: Callback invoked on error.
        :type errback: function
        :param timeout: Timeout for the operation, in seconds. Only used if blocking.
        :type timeout: float
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        return self.calibrate(CalibrateMode.AUTO, callback, errback, timeout)

    def request_new_calibration(self, callback=None, errback=None, timeout=None):
        """
        Starts a automatic motors calibration even if motors are calibrated yet.

        Examples: ::
            # Synchronous use
            arm.request_new_calibration()

            # Asynchronous use
            def calibration_callback(result):
                if result["status"] < RobotErrors.SUCCESS.value:
                    print("Calibration failed")
                else:
                    print("Calibration completed with success")

            arm.request_new_calibration(calibration_callback)

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param errback: Callback invoked on error.
        :type errback: function
        :param timeout: Timeout for the operation, in seconds. Only used if blocking.
        :type timeout: float
        :return: True if command where successfully completed, False otherwise.
                Returns always True with non blocking use.
        :rtype: Bool
        """
        self.reset_calibration()
        return self.calibrate_auto(callback, errback, timeout)

    def reset_calibration(self, timeout=2):
        """
        Resets current calibration status. A new calibration is then necessary.

        :param timeout: Timeout for the operation, in seconds.
        :type timeout: float
        :return: True if command where successfully completed, False if failed or timeout occurs..
        :rtype: Bool
        """
        request = self._services.get_trigger_request()
        self._services.request_new_calibration_service.call(request)

        start_time = time.time()
        while time.time() - start_time < timeout:
            hardware_status = self._topics.hardware_status_topic()
            if hardware_status and hardware_status.calibration_needed:
                return True
            time.sleep(0.05)
        return False

    def need_calibration(self):
        """
        Returns a bool indicating whereas the robot motors need to be calibrate.

        :return: True if calibration is needed, False otherwise.
        :rtype: bool
        """
        hardware_status = self._topics.hardware_status_topic()
        return hardware_status.calibration_needed

    # - Hardware Status

    @property
    def hardware_status(self):
        """
        Returns the hardware state client which can be used synchronously or asynchronously
        to obtain the hardware state.

        Examples: ::

            # Get last value
            arm.hardware_status()
            arm.hardware_status.value

            # Subscribe a callback
            def hs_callback(msg):
                print msg.voltage

            arm.hardware_status.subscribe(hs_callback)
            arm.hardware_status.unsubscribe()

        :return: hardware state topic instance
        :rtype: NiryoTopic
        """
        return self._topics.hardware_status_topic

    # -- Learning mode

    @property
    def learning_mode(self):
        """
        Returns the learning mode client which can be used synchronously or asynchronously
        to obtain the learning mode state.
        The learning mode client returns a boolean value.

        Examples: ::

            # Get last value
            arm.learning_mode()
            if arm.learning_mode.value:
                print("Learning mode enabled"))

            # Subscribe a callback
            def lm_callback(is_learning_mode_enabled):
                print is_learning_mode_enabled

            arm.learning_mode.subscribe(lm_callback)
            arm.learning_mode.unsubscribe()

        :return: learning mode state topic instance
        :rtype: NiryoTopic
        """
        return self._topics.learning_mode_state_topic

    def get_learning_mode(self):
        """
        Get learning mode state.

        :return: ``True`` if learning mode is on
        :rtype: bool
        """
        return self._topics.learning_mode_state_topic()

    @learning_mode.setter
    def learning_mode(self, enabled):
        """
        Set learning mode if param is ``True``, else turn it off

        :param enabled: ``True`` or ``False``
        :type enabled: bool
        """
        self.set_learning_mode(enabled)

    def set_learning_mode(self, enabled):
        """
        Set learning mode if param is ``True``, else turn it off

        :param enabled: ``True`` or ``False``
        :type enabled: bool
        :return: True if succeeded, False otherwise
        :rtype: Bool
        """
        self._check_type(enabled, bool)
        req = self._services.get_learning_mode_request(enabled)
        resp = self._services.activate_learning_mode_service.call(req)
        return resp["status"] >= RobotErrors.SUCCESS.value

    # - Get Joints/Pose

    @property
    def joints_state(self):
        """
        Get the joints state topic which can be used synchronously or asynchronously to obtain the joints state.
        The joints state topic returns a JointStateObject.

        It can be used as follows:: ::

            # Get last joint state
            joint_state = arm.joints_state()
            joint_state = arm.joints_state.value

            joint_names = arm.joints_state().name
            joint_positions = arm.joints_state().position
            joint_velocities = arm.joints_state.value.velocity

            # Raise a callback at each new value
            from __future__ import print_function

            arm.joints_state.subscribe(lambda message: print(message.position))
            arm.joints_state.unsubscribe()


        :return: Joint states topic.
        :rtype: NiryoTopic
        """
        return self._topics.joint_states_topic

    @property
    def joints(self):
        """
        Get joints value in radians

        :return: List of joints value
        :rtype: list[float]
        """
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
        return self._topics.joint_states_topic().position

    @property
    def pose(self):
        """
        Get end effector link pose as [x, y, z, roll, pitch, yaw].
        x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians

        You can also use a getter ::

            pose = robot.pose
            pose_list = robot.pose.to_list()
            x, y, z, roll, pitch, yaw = robot.pose.to_list()

        :return: end effector link pose
        :rtype: PoseObject
        """
        return self._topics.robot_state_topic()

    @property
    def get_pose(self):
        """
        Get the end effector link pose topic which can be used synchronously or asynchronously
        to obtain the end effector link pose.
        The joints state topic returns a PoseObject.
        x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians

        See below some usage ::

            pose = arm.get_pose()
            pose = arm.get_pose.value
            pose_list = arm.get_pose().to_list()
            x, y, z, roll, pitch, yaw = arm.get_pose().to_list()

            arm.get_pose.subscribe(callback)
            arm.get_pose.unsubscribe()

        :return: end effector link pose topic
        :rtype: NiryoTopic
        """
        return self._topics.robot_state_topic

    def get_pose_quat(self):
        """
        Get end effector link pose in Quaternion coordinates

        :return: Position and quaternion coordinates concatenated in a list : [x, y, z, qx, qy, qz, qw]
        :rtype: list[float]
        """
        return self._topics.robot_state_topic().quaternion

    # --  Simple Move

    @joints.setter
    def joints(self, joints):
        """
        Move robot joints. Joints are expressed in radians.

        :param joints: a list of 6 joints
        :type joints: Union[list[float], tuple[float]]
        """
        self.move_joints(joints)

    def move_joints(self, joints, callback=None):
        """
        Move robot joints. Joints are expressed in radians.
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        All lines of the next example realize the same operation: ::

            robot.joints = [0.2, 0.1, 0.3, 0.0, 0.5, 0.0]
            robot.move_joints([0.2, 0.1, 0.3, 0.0, 0.5, 0.0])

            def move_callback(_):
                print("Move completed")

            robot.move_joints([0.2, 0.1, 0.3, 0.0, 0.5, 0.0], move_callback)

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param joints: a list of 6 joints
        :type joints: Union[list[float], tuple[float]]
        :rtype: None
        """
        goal = self._actions.get_move_joints_goal(joints)
        goal.send(result_callback=callback)
        if callback is None:
            _result = goal.wait(self.__action_timeout)

    @pose.setter
    def pose(self, pose):
        """
        Move robot end effector pose to a (x, y, z, roll, pitch, yaw) pose.
        x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians

        :param pose: either a list of 6 coordinates or a ``PoseObject``
        :type pose: Union[tuple[float], list[float], PoseObject]
        """
        self.move_pose(pose)

    def move_pose(self, pose, callback=None):
        """
        Move robot end effector pose to a (x, y, z, roll, pitch, yaw) pose.
        x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        All lines of the next example realize the same operation: ::

            robot.pose = [0.2, 0.1, 0.3, 0.0, 0.5, 0.0]
            robot.move_pose([0.2, 0.1, 0.3, 0.0, 0.5, 0.0])
            robot.move_pose(PoseObject(0.2, 0.1, 0.3, 0.0, 0.5, 0.0))

            def move_callback(_):
                print("Move completed")

            robot.move_joints([0.2, 0.1, 0.3, 0.0, 0.5, 0.0], move_callback)

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param pose: either a list of 6 coordinates or a ``PoseObject``
        :type pose: Union[tuple[float], list[float], PoseObject]

        :rtype: None
        """
        pose_list = self.__args_pose_to_list(pose)
        goal = self._actions.get_move_pose_goal(pose_list)
        goal.send(result_callback=callback)
        if callback is None:
            _result = goal.wait(self.__action_timeout)

    def move_to_home_pose(self, callback=None):
        """
        Move to a position where the forearm lays on shoulder
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :rtype: None
        """
        self.move_joints([0.0, 0.3, -1.3, 0.0, 0.0, 0.0], callback)

    def go_to_sleep(self):
        """
        Go to home pose and activate learning mode

        :rtype: None
        """
        self.move_to_home_pose()
        self.set_learning_mode(True)

    def move_linear_pose(self, pose, callback=None):
        """
        Move robot end effector pose to a (x, y, z, roll, pitch, yaw) pose in a linear way
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        All lines of the next example realize the same operation: ::

            robot.move_linear_pose([0.2, 0.1, 0.3, 0.0, 0.5, 0.0])
            robot.move_linear_pose(PoseObject(0.2, 0.1, 0.3, 0.0, 0.5, 0.0))

            def move_callback(_):
                print("Move completed")

            robot.move_linear_pose([0.2, 0.1, 0.3, 0.0, 0.5, 0.0], move_callback)

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param pose: either or a list of 6 coordinates or a PoseObject
        :type pose: Union[tuple[float], list[float], PoseObject]
        :rtype: None
        """
        pose_list = self.__args_pose_to_list(pose)
        goal = self._actions.get_move_linear_pose_goal(pose_list)
        goal.send(result_callback=callback)
        _result = goal.wait(self.__action_timeout)

    def stop_move(self, callback=None, errback=None, timeout=None):
        """
        Stop a current execution of move_pose, move_joint or move_linear_pose.
        The robot will stop at its current position .
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::
            # Synchronous use
            arm.stop_move()

            # Asynchronous use
            def stop_callback(result):
                if result["status"] < RobotErrors.SUCCESS.value:
                    print("Succeeded")
                else:
                    print("Failed")

            arm.stop_move(stop_callback)

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param errback: Callback invoked on error.
        :type errback: function
        :param timeout: Timeout for the operation, in seconds. Only used if blocking.
        :type timeout: float
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        req = self._services.get_trigger_request()
        resp = self._services.stop_arm_service.call(req, callback, errback, timeout)

        if callback is not None:
            return resp["status"] >= RobotErrors.SUCCESS.value
        return True

    @property
    def get_arm_max_velocity(self):
        """
        Returns the arm max velocity client which can be used synchronously or asynchronously
        to obtain the arm max velocity.
        The arm max velocity client returns an integer value.

        Examples: ::

            # Get last value
            arm.get_arm_max_velocity()
            arm.get_arm_max_velocity.value

            # Subscribe a callback
            def velocity_callback(velocity_percentage):
                print velocity_percentage

            arm.get_arm_max_velocity.subscribe(velocity_callback)
            arm.get_arm_max_velocity.unsubscribe()

        :return: arm velocity topic instance
        :rtype: NiryoTopic
        """
        return self._topics.max_velocity_scaling_factor_topic

    def set_arm_max_velocity(self, percentage_speed):
        """
        Limit arm max velocity to a percentage of its maximum velocity

        :param percentage_speed: Should be between 1 & 100
        :type percentage_speed: int
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        self._check_range_belonging(percentage_speed, 1, 100)
        req = self._services.get_max_velocity_scaling_factor_request(percentage_speed)
        return self._services.set_max_velocity_scaling_factor_service.call(req)["status"] >= RobotErrors.SUCCESS.value

    # - Shift Pose

    def shift_pose(self, axis, shift_value, callback=None):
        """
        Shift robot end effector pose along one axis
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::
            self.arm.shift_pose(RobotAxis.X, 0.05)
            self.arm.shift_pose(RobotAxis.Y, -0.05)
            self.arm.shift_pose(RobotAxis.Z, 0.1)
            self.arm.shift_pose(RobotAxis.ROLL, 1.57)
            self.arm.shift_pose(RobotAxis.PITCH, -1.57)
            self.arm.shift_pose(RobotAxis.YAW, 0.78)

            def move_callback(_):
                print("Move completed")

            self.arm.shift_pose(RobotAxis.X, 0.1, move_callback)


        :param axis: Axis along which the robot is shifted
        :type axis: RobotAxis
        :param shift_value: In meter for X/Y/Z and radians for roll/pitch/yaw
        :type shift_value: float
        :param callback: Callback invoked on successful execution.
        :type callback: function
        :rtype: None
        """
        self._check_enum_belonging(axis, RobotAxis)
        shift_value = self._transform_to_type(shift_value, float)

        goal = self._actions.get_shift_pose_goal(axis.value, shift_value)
        goal.send(result_callback=callback)
        if callback is None:
            _result = goal.wait(self.__action_timeout)

    # - Jog

    def set_jog_control(self, enabled):
        """
        Set jog control mode if param is True, else turn it off

        :param enabled: ``True`` or ``False``
        :type enabled: Bool
        :return: True if command where successfully completed, False otherwise.
        :rtype: Bool
        """
        self._check_type(enabled, bool)
        req = self._services.get_enable_jog_request(enabled)
        return self._services.enable_jog_controller_service.call(req)["status"] >= RobotErrors.SUCCESS.value

    def jog_joints(self, joints_offset, callback=None, errback=None, timeout=None):
        """
        Jog robot joints'.
        Jog corresponds to a shift without motion planning.
        Values are expressed in radians.
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::

            arm.jog_joints([0.1, 0.0, 0.5, 0.0, 0.0, -1.57])

            def jog_callback(_):
                print("Jog completed")
                arm.set_jog_control(False) # Disable Jog interface

            arm.jog_joints([0.1, 0.0, 0.5, 0.0, 0.0, -1.57], jog_callback)


        :param joints_offset: a list of 6 joints offset
        :type joints_offset: Union[list[float], tuple[float]]
        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param errback: Callback invoked on error.
        :type errback: function
        :param timeout: Timeout for the operation, in seconds. Only used if blocking.
        :type timeout: float
        :rtype: None
        """
        joints_off = self.__args_joints_to_list(joints_offset)
        req = self._services.get_jog_request(JogShift.JOINTS_SHIFT.value, joints_off)
        self._services.jog_shift_service.call(req, callback, errback, timeout)

    def jog_pose(self, pose_offset, callback=None, errback=None, timeout=None):
        """
        Jog robot end effector pose
        Jog corresponds to a shift without motion planning
        Arguments are [dx, dy, dz, d_roll, d_pitch, d_yaw]
        dx, dy & dz are expressed in meters / d_roll, d_pitch & d_yaw are expressed in radians
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::

            arm.jog_pose([0.01, 0.0, 0.05, 0.0, 0.0, -1.57])

            def jog_callback(_):
                print("Jog completed")
                arm.set_jog_control(False) # Disable Jog interface

            arm.jog_pose([0.1, 0.0, 0.5, 0.0, 0.0, -1.57], jog_callback)


        :param pose_offset: a list of 6 offset
        :type pose_offset: Union[list[float], tuple[float]]
        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param errback: Callback invoked on error.
        :type errback: function
        :param timeout: Timeout for the operation, in seconds. Only used if blocking.
        :type timeout: float
        :rtype: None
        """
        pose_offset_list = self.__args_pose_to_list(pose_offset)
        req = self._services.get_jog_request(JogShift.POSE_SHIFT.value, pose_offset_list)
        self._services.jog_shift_service.call(req, callback, errback, timeout)

    # -- Kinematics

    def forward_kinematics(self, *args):
        """
        Compute forward kinematics of a given joints configuration and give the
        associated spatial pose

        Examples: ::
            pose_obj = arm.forward_kinematics(1.57, 0.0, 0.0, 0.78, 0.0, -1.57)
            pose_obj = arm.forward_kinematics([1.57, 0.0, 0.0, 0.78, 0.0, -1.57])

        :param args: either 6 args (1 for each joints) or a list of 6 joints
        :type args: Union[list[float], tuple[float]]
        :rtype: PoseObject
        """
        joints = self.__args_joints_to_list(*args)
        request = self._services.get_forward_kinematics_request(joints)
        response = self._services.forward_kinematics_service.call(request)

        pose_array = self._services.pose_dict_to_list(response["pose"])
        pose_object = PoseObject(*pose_array)
        return pose_object

    def inverse_kinematics(self, *args):
        """
        Compute inverse kinematics

        Examples: ::
            joint_list = arm.inverse_kinematics(0.2, 0.0, 0.3, 0.0, 1.57, 0.0)
            joint_list = arm.inverse_kinematics([0.2, 0.0, 0.3, 0.0, 1.57, 0.0])
            joint_list = arm.inverse_kinematics(PoseObject(0.2, 0.0, 0.3, 0.0, 1.57, 0.0))

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
