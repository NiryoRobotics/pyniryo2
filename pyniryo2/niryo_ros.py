# Python libraries
import roslibpy
import socket
import time


class NiryoRosTimeoutException(Exception):
    pass


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
        self.port = port
        self.ip_address = ip_address
        super(NiryoRos, self).__init__(host=ip_address, port=port)

        self.__connected = False
        self.__pyniryo2_ip = socket.gethostbyname(socket.gethostname())

        self.__pyniryo_ping_service = roslibpy.Service(self, '/niryo_robot_pyniryo2/ping', 'niryo_robot_msgs/GetString')

        self.run()
        time.sleep(0.1)
        self.__pyniryo_ping_service.advertise(self.__ping_callback)
        #self.wait_for_connection()
        time.sleep(2)

    def wait_for_connection(self):
        start_time = time.time()
        while not self.__connected:
            time.sleep(0.1)
            if time.time() - start_time > 15:
                raise NiryoRosTimeoutException(
                    "Connection timeout on ip {} and port {}".format(self.ip_address, self.port))
    #
    def __ping_callback(self, _request, response):
        response['value'] = self.__pyniryo2_ip
        self.__connected = True
        return True
