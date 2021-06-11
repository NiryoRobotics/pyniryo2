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

"""
/niryo_robot_arm_commander/is_active
/niryo_robot_arm_commander/linear_trajectory/activate
/niryo_robot_arm_commander/set_max_velocity_scaling_factor
/niryo_robot_arm_commander/stop_command
"""
