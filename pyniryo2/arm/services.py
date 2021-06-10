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