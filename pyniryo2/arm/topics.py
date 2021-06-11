from pyniryo2.niryo_topic import NiryoTopic


class ArmTopics(object):

    def __init__(self, client):
        self.__client = client

        self.joint_states_topic = NiryoTopic(self.__client,
                                                      '/joint_states',
                                                      'sensor_msgs/JointState')

        self.robot_state_topic = NiryoTopic(self.__client,
                                                      '/niryo_robot/robot_state',
                                                      'niryo_robot_msgs/RobotState')

        self.hardware_status_topic = NiryoTopic(self.__client,
                                                      '/niryo_robot_hardware_interface/hardware_status',
                                                      'niryo_robot_msgs/HardwareStatus')

        self.learning_mode_state_topic = NiryoTopic(self.__client,
                                                      '/niryo_robot/learning_mode/state',
                                                      'std_msgs/Bool')

        self.max_velocity_scaling_factor_topic = NiryoTopic(self.__client,
                                                      '/niryo_robot/max_velocity_scaling_factor',
                                                      'std_msgs/Int32')