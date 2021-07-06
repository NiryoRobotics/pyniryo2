# - Imports
from __future__ import print_function

# Python libraries
import roslibpy
import time

# Communication imports
from .arm.arm import Arm
from .io.io import IO
from .pick_place.pick_place import PickPlace
from .saved_poses.saved_poses import SavedPoses
from .tool.tool import Tool
from .trajectories.trajectories import Trajectories
from .vision.vision import Vision


class NiryoRobot(object):
    def __init__(self, ip_address="127.0.0.1", port=9090):
        self.__host = None
        self.__port = None
        self.__client = None

        self.run(ip_address, port)

        self.__arm = Arm(self.__client)
        self.__io = IO(self.__client)
        self.__saved_poses = SavedPoses(self.__client)
        self.__tool = Tool(self.__client)
        self.__trajectories = Trajectories(self.__client)
        self.__pick_place = PickPlace(self.__client, self.__arm, self.__tool, self.__trajectories)
        self.__vision = Vision(self.__client, self.__arm, self.__tool)

    def __del__(self):
        if self.__client:
            self.terminate()

    def __str__(self):
        return "Niryo Robot"

    def __repr__(self):
        return self.__str__()

    def run(self, ip_address="127.0.0.1", port=9090):
        self.__host = ip_address
        self.__port = port

        self.__client = roslibpy.Ros(host=self.__host, port=self.__port)
        self.__client.run()

    def terminate(self):
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

    @property
    def io(self):
        return self.__io

    @property
    def pick_place(self):
        return self.__pick_place

    @property
    def saved_poses(self):
        return self.__saved_poses

    @property
    def tool(self):
        return self.__tool

    @property
    def trajectories(self):
        return self.__trajectories

    @property
    def vision(self):
        return self.__vision

