# - Imports
from __future__ import print_function

# Python libraries
import roslibpy
import time

# Communication imports
from .exceptions import *
from pyniryo2.arm.arm import Arm


class NiryoRobot(object):
    def __init__(self, host="127.0.0.1", port=9090):
        self.__host = None
        self.__port = None
        self.__client = None

        self.connect(host, port)

        self.__arm = Arm(self.__client)

    def __del__(self):
        if self.__client:
            self.disconnect()

    def __str__(self):
        return "Niryo Robot"

    def __repr__(self):
        return self.__str__()

    def connect(self, host="127.0.0.1", port=9090):
        self.__host = host
        self.__port = port

        self.__client = roslibpy.Ros(host=self.__host, port=self.__port)
        self.__client.run()

    def disconnect(self):
        self.__client.terminate()

    @staticmethod
    def wait(duration):
        """
        Wait for a certain time

        :param duration: duration in seconds
        :type duration: float
        :rtype: None
        """
        time.sleep(duration)

    @property
    def arm(self):
        return self.__arm

