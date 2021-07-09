# - Imports
from __future__ import print_function

# Python libraries
import roslibpy
import time

# Communication imports
from .arm.arm import Arm
from .conveyor.conveyor import Conveyor
from .io.io import IO
from .pick_place.pick_place import PickPlace
from .saved_poses.saved_poses import SavedPoses
from .tool.tool import Tool
from .trajectories.trajectories import Trajectories
from .vision.vision import Vision


class NiryoRobot(object):
    def __init__(self, ip_address="127.0.0.1", port=9090):
        """
        Connect your orbot to your computer: ::

            robot_simulation = NiryoRobot("127.0.0.1") # Simulation

            robot_hotpot = NiryoRobot("10.10.10.10") # Hotspot

            robot_ethernet = NiryoRobot("169.254.200.201") # Ethernet

        :param ip_address:
        :type ip_address:
        :param port:
        :type port:
        """
        self.__host = None
        self.__port = None
        self.__client = None

        self.__vision = None
        self.__pick_place = None
        self.__trajectories = None
        self.__tool = None
        self.__saved_poses = None
        self.__io = None
        self.__conveyor = None
        self.__arm = None

        self.run(ip_address, port)

        self.__arm = Arm(self.__client)
        self.__conveyor = Conveyor(self.__client)
        self.__io = IO(self.__client)
        self.__saved_poses = SavedPoses(self.__client)
        self.__tool = Tool(self.__client)
        self.__trajectories = Trajectories(self.__client)
        self.__pick_place = PickPlace(self.__client, self.__arm, self.__tool, self.__trajectories)
        self.__vision = Vision(self.__client, self.__arm, self.__tool)

    def __del__(self):
        del self.__vision
        del self.__pick_place
        del self.__trajectories
        del self.__tool
        del self.__saved_poses
        del self.__io
        del self.__conveyor
        del self.__arm

        self.end()

    def __str__(self):
        return "Niryo Robot"

    def __repr__(self):
        return self.__str__()

    def run(self, ip_address="127.0.0.1", port=9090):
        """
        Connect to your robot and ROS
        This function is already called at the initialization of the class.
        It is therefore not necessary to call it again, except to reconnect the robot. ::

            # Start
            robot = NiryoRobot("10.10.10.10")

            # End
            robot.end()

            # Reconnect
            robot_hotpot.run("10.10.10.10")

        :type ip_address: str
        :type port: int
        :rtype: None
        """
        self.__host = ip_address
        self.__port = port

        self.__client = roslibpy.Ros(host=self.__host, port=self.__port)
        self.__client.run()

    def end(self):
        """
        Disconnect from your robot and ROS: ::

            # Start
            robot = NiryoRobot("10.10.10.10")

            # End
            robot.end()

        :rtype: None
        """
        if self.__client is not None and self.__client.is_connected:
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
    def conveyor(self):
        return self.__conveyor

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
