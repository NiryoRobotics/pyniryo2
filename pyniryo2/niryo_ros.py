# Python libraries
import roslibpy
import socket

from .niryo_topic import NiryoTopic


class NiryoRos(roslibpy.Ros):
    def __init__(self, ip_address="127.0.0.1", port=9090):
        """
        Connect to your computer to ros: ::

            ros_instance = NiryoRos("127.0.0.1") # Simulation

            ros_instance = NiryoRos("10.10.10.10") # Hotspot

            ros_instance = NiryoRos("169.254.200.201") # Ethernet

        :param ip_address: ip of the ros master
        :type ip_address: string
        :param port: usually 9090
        :type port: int
        """

        super(NiryoRos, self).__init__(host=ip_address, port=port)

        self.__pyniryo_ping_topic = NiryoTopic(self,
                                               '/niryo_robot_pyniryo2/ping',
                                               'std_msgs/Empty')

        self.__pyniryo_pong_topic = roslibpy.Topic(self, '/chatter', 'std_msgs/String')
        self.__pyniryo_pong_topic.subscribe(self.__ping_callback)

        self.__pyniryo_ping_topic = NiryoTopic(self,
                                               '/niryo_robot_pyniryo2/pong',
                                               'std_msgs/String', )

        self.run()

    def __ping_callback(self, *_):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        self.__pyniryo_ping_topic.publish({'data': local_ip})
