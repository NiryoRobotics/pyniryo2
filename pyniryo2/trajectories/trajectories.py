# - Imports
from __future__ import print_function

# Python libraries
import roslibpy
import time

# Communication imports
from pyniryo2.robot_commander import RobotCommander

from pyniryo2.trajectories.services import TrajectoriesServices
# from pyniryo2.trajectories.topics import TrajectoriesTopics
from pyniryo2.trajectories.actions import TrajectoriesActions


class Trajectories(RobotCommander):
    # --- Public functions --- #
    def __init__(self, client):
        super(Trajectories, self).__init__(client)

        self._services = TrajectoriesServices(self._client)
        # self._topics = TrajectoriesTopics(self._client)
        self._actions = TrajectoriesActions(self._client)

        self.__action_timeout = 10

    # - Main purpose
    def get_trajectory_saved(self, trajectory_name):
        """
        Get saved trajectory from robot intern storage
        Will raise error if position does not exist

        :param trajectory_name: name of the trajectory
        :type trajectory_name: str
        :raises NiryoRosWrapperException: If trajectory file doesn't exist TODO: what does it raise?
        :return: list of [x, y, z, qx, qy, qz, qw]
        :rtype: list[list[float]]
        """
        self._check_type(trajectory_name, str)
        req = self._services.get_trajectory_from_name_request(trajectory_name)
        response = self._services.get_trajectory_from_name_service.call(req)
        pose_quat_list = self._services.trajectory_dict_to_list(response["list_poses"])
        return pose_quat_list
        

    def execute_trajectory_saved(self, trajectory_name):
        return

    def execute_trajectory_from_poses(self, list_poses, dist_smoothing=0.0):
        return
    
    def save_trajectory(self, trajectory_name, list_poses):
        return
    
    def delete_trajectory(self, trajectory_name):
        return
    
    def get_saved_trajectory_list(self):
        return
   