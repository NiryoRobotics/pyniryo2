from pyniryo2.niryo_topic import NiryoTopic


class ArmTopics(object):

    def __init__(self, client):
        self.__client = client

        self.joint_states_topic = NiryoTopic(self.__client,
                                                      '/joint_states',
                                                      'sensor_msgs/JointState')

        self.hardware_status_topic = NiryoTopic(self.__client,
                                                      '/niryo_robot_hardware_interface/hardware_status',
                                                      'niryo_robot_msgs/HardwareStatus')