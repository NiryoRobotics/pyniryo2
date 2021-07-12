# - Imports
import numpy as np

from pyniryo2.robot_commander import RobotCommander
from pyniryo2.objects import PoseObject

from .services import TrajectoriesServices
from .actions import TrajectoriesActions


class Trajectories(RobotCommander):
    # --- Public functions --- #
    def __init__(self, client):
        super(Trajectories, self).__init__(client)

        self._services = TrajectoriesServices(self._client)
        self._actions = TrajectoriesActions(self._client)

        self.__action_timeout = 60

    # - Main purpose
    def get_trajectory_saved(self, trajectory_name):
        """
        Get saved trajectory from robot intern storage
        Will raise error if position does not exist

        Example: ::

            trajectories.get_trajectory_saved("trajectory_01")

        :param trajectory_name: name of the trajectory
        :type trajectory_name: str
        :raises NiryoRosWrapperException: If trajectory file doesn't exist TODO: what does it raise?
        :return: list of [x, y, z, qx, qy, qz, qw]
        :rtype: list[list[float]]
        """
        self._check_type(trajectory_name, str)

        req = self._services.get_trajectory_from_name_request(trajectory_name)
        response = self._services.get_trajectory_from_name_service.call(req)
        self._check_result_status(response)
        pose_quat_list = self._services.trajectory_dict_to_list(response["list_poses"])
        return pose_quat_list

    def execute_trajectory_saved(self, trajectory_name, dist_smoothing=0.0, callback=None):
        """
        Execute trajectory from Ned's memory
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::

            trajectories.execute_trajectory_saved("trajectory_01")
            trajectories.execute_trajectory_saved("trajectory_01", dist_smoothing=0.02)

            from threading import Event
            trajectory_event = Event()
            trajectory_event.clear()

            def trajectory_callback(result):
                print(result)
                trajectory_event.set()

            trajectories.execute_trajectory_saved("trajectory_01", callback=trajectory_callback)
            trajectory_event.wait()

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param dist_smoothing: Distance from waypoints before smoothing trajectory
        :type dist_smoothing: float
        :type trajectory_name: str
        :rtype: None
        """
        trajectory = self.get_trajectory_saved(trajectory_name)
        self.execute_trajectory_from_poses(trajectory, dist_smoothing, callback)

    def execute_trajectory_from_poses(self, list_poses, dist_smoothing=0.0, callback=None):
        """
        Execute trajectory from list of poses
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::

            trajectory = [[0.3, 0.1, 0.3, 0., 0., 0., 1.],
                          [0.3, -0.1, 0.3, 0., 0., 0., 1.],
                          [0.3, -0.1, 0.4, 0., 0., 0., 1.],
                          [0.3, 0.1, 0.4, 0., 0., 0., 1.]]

            trajectories.execute_trajectory_from_poses(trajectory)
            trajectories.execute_trajectory_from_poses(trajectory, dist_smoothing=0.02)
            trajectories.execute_trajectory_from_poses([[0.3, 0.1, 0.3, 0., 0., 0., 1.], #[x,y,z,qx,qy,qz,qw]
                                                 PoseObject(0.3, -0.1, 0.3, 0., 0., 0.),
                                                 [0.3, -0.1, 0.4, 0., 0., 0.], #[x,y,z,roll,pitch,yaw]
                                                 PoseObject(0.3, 0.1, 0.4, 0., 0., 0.)])

            from threading import Event
            trajectory_event = Event()
            trajectory_event.clear()

            def trajectory_callback(result):
                print(result)
                trajectory_event.set()

            trajectories.execute_trajectory_from_poses(trajectory, callback=trajectory_callback)
            trajectory_event.wait()

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param list_poses: List of: [x,y,z,qx,qy,qz,qw] or [x,y,z,roll,pitch,yaw] or PoseObject
        :type list_poses: list[Union[tuple[float], list[float], PoseObject]]
        :param dist_smoothing: Distance from waypoints before smoothing trajectory
        :type dist_smoothing: float
        :rtype: None
        """
        self._check_range_belonging(dist_smoothing, 0.0, np.Inf)
        trajectory = self.__list_pose_to_trajectory(list_poses)
        goal = self._actions.get_execute_trajectories_goal(trajectory, dist_smoothing)
        goal.send(result_callback=callback)
        if callback is None:
            _result = goal.wait(self.__action_timeout)

    def save_trajectory(self, trajectory_name, list_poses):
        """
        Save trajectory in robot's memory

        Examples: ::

            trajectories.save_trajectory("trajectory_1", [[0.3, 0.1, 0.3, 0., 0., 0., 1.], #[x,y,z,qx,qy,qz,qw]
                                                          [0.3, -0.1, 0.3, 0., 0., 0., 1.], #[x,y,z,qx,qy,qz,qw]
                                                          [0.3, -0.1, 0.4, 0., 0., 0., 1.], #[x,y,z,qx,qy,qz,qw]
                                                          [0.3, 0.1, 0.4, 0., 0., 0., 1.]]) #[x,y,z,qx,qy,qz,qw]

            trajectories.execute_trajectory_from_poses([[0.3, 0.1, 0.3, 0., 0., 0., 1.], #[x,y,z,qx,qy,qz,qw]
                                                 PoseObject(0.3, -0.1, 0.3, 0., 0., 0.),
                                                 [0.3, -0.1, 0.4, 0., 0., 0.], #[x,y,z,roll,pitch,yaw]
                                                 PoseObject(0.3, 0.1, 0.4, 0., 0., 0.)])

        :type trajectory_name: str
        :param list_poses: List of: [x,y,z,qx,qy,qz,qw] or [x,y,z,roll,pitch,yaw] or PoseObject
        :type list_poses: list[Union[tuple[float], list[float], PoseObject]]
        :rtype: None
        """
        self._check_type(trajectory_name, str)
        self._check_type(list_poses, list)

        saved_poses = self.__list_pose_to_trajectory(list_poses)
        req = self._services.save_trajectory_request(trajectory_name, saved_poses)
        response = self._services.save_delete_trajectory_service.call(req)
        self._check_result_status(response)

    def delete_trajectory(self, trajectory_name):
        """
        Delete trajectory from robot's memory

        Example: ::

            if "trajectory_1" in trajectories.get_saved_trajectory_list():
                trajectories.delete_trajectory("trajectory_1")

        :type trajectory_name: str
        :rtype: None
        """
        self._check_type(trajectory_name, str)

        req = self._services.delete_trajectory_request(trajectory_name)
        response = self._services.save_delete_trajectory_service.call(req)
        self._check_result_status(response)

    def get_saved_trajectory_list(self):
        """
        Get list of trajectories' name saved in robot memory

        Example: ::

            if "trajectory_1" in trajectories.get_saved_trajectory_list():
                trajectories.delete_trajectory("trajectory_1")

        :rtype: list[str]
        """
        req = self._services.get_saved_trajectory_list_request()
        response = self._services.get_trajectory_list_service.call(req)
        return self._services.get_saved_trajectory_list_response_to_list(response)

    def __list_pose_to_trajectory(self, list_poses):
        """
        Convert a list of [x,y,z,qx,qy,qz,qw], [x,y,z,roll,pitch,yaw] and PoseObjects into a [x,y,z,qx,qy,qz,qw] list

        :param list_poses: List of: [x,y,z,qx,qy,qz,qw] or [x,y,z,roll,pitch,yaw] or PoseObject
        :type list_poses: list[Union[tuple[float], list[float], PoseObject]]
        :return: list[[x,y,z,qx,qy,qz,qw]] which represents a trajectory from the list_poses
        :rtype: list[list[float]]
        """
        self._check_type(list_poses, list)
        trajectory = []
        for pose in list_poses:
            if isinstance(pose, PoseObject):
                trajectory.append(pose.quaternion_pose)
            else:
                self._check_type(pose, list)
                if len(pose) == 7:
                    trajectory.append(self._map_list(pose[:], float))
                elif len(pose) == 6:
                    trajectory.append(PoseObject(*pose).quaternion_pose)
                else:
                    self._raise_exception("7 parameters expected in a pose [x,y,z,qx,qy,qz,qw], or  "
                                          "6 parameters expected in a pose [x,y,z,roll,pitch,yaw], or"
                                          "PoseObject expected in a pose [x,y,z,roll,pitch,yaw], "
                                          "{} given".format(pose))
        return trajectory
