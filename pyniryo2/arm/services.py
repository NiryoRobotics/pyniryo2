import roslibpy


class ArmServices(object):

    def __init__(self, client):
        self.__client = client

        self.request_calibration_service = roslibpy.Service(self.__client,
                                                            '/niryo_robot/joints_interface/calibrate_motors',
                                                            'niryo_robot_msgs/SetInt')

        self.request_new_calibration_service = roslibpy.Service(self.__client,
                                                                '/niryo_robot/joints_interface/request_new_calibration',
                                                                'niryo_robot_msgs/Trigger')

        self.activate_learning_mode_service = roslibpy.Service(self.__client,
                                                               '/niryo_robot/learning_mode/activate',
                                                               'niryo_robot_msgs/SetBool')

        self.forward_kinematics_service = roslibpy.Service(self.__client,
                                                           '/niryo_robot/kinematics/forward',
                                                           'niryo_robot_arm_commander/GetFK')

        self.inverse_kinematics_service = roslibpy.Service(self.__client,
                                                           '/niryo_robot/kinematics/inverse',
                                                           'niryo_robot_arm_commander/GetIK')

        self.set_max_velocity_scaling_factor_service = roslibpy.Service(self.__client,
                                                                        '/niryo_robot_arm_commander/set_max_velocity_scaling_factor',
                                                                        'niryo_robot_msgs/SetInt')

        self.enable_jog_controller_service = roslibpy.Service(self.__client,
                                               '/niryo_robot/jog_interface/enable',
                                               'niryo_robot_msgs/SetBool')

        self.jog_shift_service = roslibpy.Service(self.__client,
                                                              '/niryo_robot/jog_interface/jog_shift_commander',
                                                              'niryo_robot_commander/JogShift')

        self.stop_arm_service = roslibpy.Service(self.__client,
                                                              '/niryo_robot_arm_commander/stop_command',
                                                              'niryo_robot_msgs/Trigger')


    @staticmethod
    def get_trigger_request():
        return roslibpy.ServiceRequest()

    @staticmethod
    def get_learning_mode_request(enabled):
        """
        Set learning mode if param is ``True``, else turn it off

        :param enabled: ``True`` or ``False``
        :type enabled: bool
        :rtype: None
        """
        return roslibpy.ServiceRequest({"value": enabled})

    @staticmethod
    def get_max_velocity_scaling_factor_request(percentage):
        return roslibpy.ServiceRequest({"value": percentage})

    @staticmethod
    def get_enable_jog_request(enabled):
        return roslibpy.ServiceRequest({"value": enabled})

    @staticmethod
    def get_jog_request(cmd_type, shift_values):
        return roslibpy.ServiceRequest({"cmd": cmd_type, "shift_values": shift_values})

    @staticmethod
    def get_forward_kinematics_request(joint_list):
        return roslibpy.ServiceRequest({"joints": joint_list})

    @staticmethod
    def get_inverse_kinematics_request(pose_list):
        pose_msg = ArmServices.pose_list_to_dict(pose_list)
        return roslibpy.ServiceRequest({"pose": pose_msg})

    @staticmethod
    def pose_list_to_dict(pose_list):
        return {"position": {"x": pose_list[0], "y": pose_list[1], "z": pose_list[2]},
                "rpy": {"roll": pose_list[3], "pitch": pose_list[4], "yaw": pose_list[5]}}

