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
from .sound.sound import Sound
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
        self.__sound = None
        self.__saved_poses = None
        self.__io = None
        self.__conveyor = None
        self.__arm = None

        self.run(ip_address, port)

        self.__arm = Arm(self.__client)
        self.__conveyor = Conveyor(self.__client)
        self.__io = IO(self.__client)
        self.__saved_poses = SavedPoses(self.__client)
        self.__sound = Sound(self.__client)
        self.__tool = Tool(self.__client)
        self.__trajectories = Trajectories(self.__client)
        self.__pick_place = PickPlace(self.__client, self.__arm, self.__tool, self.__trajectories)
        self.__vision = Vision(self.__client, self.__arm, self.__tool)

    def __del__(self):
        del self.__vision
        del self.__pick_place
        del self.__trajectories
        del self.__tool
        del self.__sound
        del self.__saved_poses
        del self.__io
        del self.__conveyor
        del self.__arm

        self.end()

    def __str__(self):
        return "Niryo Robot"

    def __repr__(self):
        return self.__str__()

    @property
    def client(self):
        """
        Get the ROS client: https://roslibpy.readthedocs.io/en/latest/reference/index.html#roslibpy.Ros

        :return: ROS client
        :rtype: roslibpy.Ros
        """
        return self.__client

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
        """
        Access to the Arm API

        Example: ::

            robot = NiryoRobot(<robot_ip_address>)
            robot.arm.calibrate_auto()
            robot.arm.move_joints([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        :rtype: Arm
        """
        return self.__arm

    @property
    def conveyor(self):
        """
        Access to the Conveyor API

        Example: ::

            robot = NiryoRobot(<robot_ip_address>)
            conveyor_id = robot.conveyor.set_conveyor()
            robot.conveyor.run_conveyor(conveyor_id)

        :rtype: Conveyor
        """
        return self.__conveyor

    @property
    def io(self):
        """
        Access to the I/Os API

        Example: ::

            robot = NiryoRobot(<robot_ip_address>)
            robot.io.set_pin_mode(PinID.GPIO_1A, PinMode.INPUT)
            robot.io.digital_write(PinID.GPIO_1A, PinState.HIGH)

        :rtype: IO
        """
        return self.__io

    @property
    def pick_place(self):
        """
        Access to the PickPlace API

        Example: ::

            robot = NiryoRobot(<robot_ip_address>)
            robot.pick_place.pick_from_pose([0.2, 0.0, 0.1, 0.0, 1.57, 0.0])
            robot.pick_place.place_from_pose([0.0, 0.2, 0.1, 0.0, 1.57, 0.0])

        :rtype: PickPlace
        """
        return self.__pick_place

    @property
    def saved_poses(self):
        """
        Access to the SavedPoses API

        Example: ::

            robot = NiryoRobot(<robot_ip_address>)
            pose_name_list = robot.saved_poses.get_saved_pose_list()
            robot.saved_poses.get_pose_saved(pose_name_list[0])

        :rtype: SavedPoses
        """
        return self.__saved_poses
    
    @property
    def sound(self):
        """
        Access to the Sound API

        Example: ::

        :rtype: Sound
        """
        return self.__sound

    @property
    def tool(self):
        """
        Access to the Tool API

        Example: ::

            robot = NiryoRobot(<robot_ip_address>)
            robot.tool.update_tool()
            robot.tool.grasp_with_tool()
            robot.tool.release_with_tool()

        :rtype: Tool
        """
        return self.__tool

    @property
    def trajectories(self):
        """
        Access to the Trajectories API

        Example: ::

            robot = NiryoRobot(<robot_ip_address>)
            trajectories = robot.trajectories.get_saved_trajectory_list()
            if len(trajectories) > 0:
                robot.trajectories.execute_trajectory_saved(trajectories[0])

        :rtype: Trajectories
        """
        return self.__trajectories

    @property
    def vision(self):
        """
        Access to the Vision API

        Example: ::

            robot = NiryoRobot(<robot_ip_address>)
            robot.vision.vision_pick("workspace_1", 0.0, ObjectShape.ANY, ObjectColor.ANY)
            robot.vision.detect_object("workspace_1", ObjectShape.ANY, ObjectColor.ANY)

        :rtype: Vision
        """
        return self.__vision
