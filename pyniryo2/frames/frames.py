# - Imports
import numpy as np
import roslibpy
import time

from pyniryo2.robot_commander import RobotCommander
from pyniryo2.utils import point_list_to_dict

from .services import FramesServices

class Frames(RobotCommander):
    # --- Public functions --- #
    def __init__(self, client):
        super(Frames, self).__init__(client)

        self._services = FramesServices(self._client)

    # Main purpose
    def get_saved_dynamic_frame_list(self):
        """
        Get list of saved dynamic frames

        Example: ::

            list_frame, list_desc = robot.frames.get_saved_dynamic_frame_list()
            print(list_frame)
            print(list_desc)

        :return: list of dynamic frames name, list of description of dynamic frames
        :rtype: list[str], list[str]
        """
        req = self._services.get_saved_dynamic_frame_list_request()
        response = self._services.get_frame_list_service.call(req)
        return self._services.get_saved_dynamic_frame_list_response_to_list(response)

    def get_saved_dynamic_frame(self, frame_name):
        """
        Get name, description and pose of a dynamic frame

        Example: ::

            frame = robot.frames.get_saved_dynamic_frame("default_frame")

        :param frame_name: name of the frame
        :type frame_name: str
        :return: name, description, position and orientation of a frame
        :rtype: list[str, str, list[float]]
        """
        self._check_type(frame_name, str)
        req = self._services.get_dynamic_frame_from_name_request(frame_name)
        response = self._services.get_frame_from_name_service.call(req)
        self._check_result_status(response)

        return self._services.get_dynamic_frame_from_name_response_to_list(response)

    def save_dynamic_frame_from_poses(self, frame_name, description, pose_origin, pose_x, pose_y):
        """
        Create a dynamic frame with 3 poses (origin, x, y)

        Example: ::

            pose_o = [0.1, 0.1, 0.1, 0, 0, 0]
            pose_x = [0.2, 0.1, 0.1, 0, 0, 0]
            pose_y = [0.1, 0.2, 0.1, 0, 0, 0]

            robot.frames.save_dynamic_frame_from_poses("name", "une description test", pose_o, pose_x, pose_y)

        :param frame_name: name of the frame
        :type frame_name: str
        :param description: description of the frame
        :type description: str
        :param pose_origin: pose of the origin of the frame
        :type pose_origin: list[float] [x, y, z, roll, pitch, yaw]
        :param pose_x: pose of the point x of the frame
        :type pose_x: list[float] [x, y, z, roll, pitch, yaw]
        :param pose_y: pose of the point y of the frame
        :type pose_y: list[float] [x, y, z, roll, pitch, yaw]
        :return: status, message
        :rtype: (int, str)
        """
        self._check_type(frame_name, str)
        self._check_type(description, str)
        self._check_type(pose_origin, list)
        self._check_type(pose_x, list)
        self._check_type(pose_y, list)

        pose_list = [self._args_pose_to_list(pose) for pose in (pose_origin, pose_x, pose_y)]

        points_list = [point_list_to_dict(point) for point in pose_list]

        dynamic_frame = {"name": frame_name, "description": description, "points": points_list}

        req = self._services.save_dynamic_frame_from_points_request(dynamic_frame)
        response = self._services.manage_frame_service.call(req)
        self._check_result_status(response)

    def save_dynamic_frame_from_points(self, frame_name, description, point_origin, point_x, point_y):
        """
        Create a dynamic frame with 3 points (origin, x, y)

        Example: ::

            point_o = [-0.1, -0.1, 0.1]
            point_x = [-0.2, -0.1, 0.1]
            point_y = [-0.1, -0.2, 0.1]

            robot.frames.save_dynamic_frame_from_points("name", "une description test", point_o, point_x, point_y)

        :param frame_name: name of the frame
        :type frame_name: str
        :param description: description of the frame
        :type description: str
        :param point_origin: origin point of the frame
        :type point_origin: list[float] [x, y, z]
        :param point_x: point x of the frame
        :type point_x: list[float] [x, y, z]
        :param point_y: point y of the frame
        :type point_y: list[float] [x, y, z]
        :return: status, message
        :rtype: (int, str)
        """
        self._check_type(frame_name, str)
        self._check_type(description, str)
        self._check_type(point_origin, list)
        self._check_type(point_x, list)
        self._check_type(point_y, list)

        points_list_raw = [point_origin, point_x, point_y]

        points_list = [point_list_to_dict(point) for point in points_list_raw]

        dynamic_frame = {"name": frame_name, "description": description, "points": points_list}

        req = self._services.save_dynamic_frame_from_points_request(dynamic_frame)
        response = self._services.manage_frame_service.call(req)
        self._check_result_status(response)

    def edit_dynamic_frame(self, frame_name, new_frame_name,  new_description):
        """
        Modify a dynamic frame

        Example: ::

            robot.frames.edit_dynamic_frame("name", "new_name", "new description")

        :param frame_name: name of the frame
        :type frame_name: str
        :param new_frame_name: new name of the frame
        :type new_frame_name: str
        :param new_description: new description of the frame
        :type new_description: str
        :return: status, message
        :rtype: (int, str)
        """
        self._check_type(frame_name, str)
        self._check_type(new_frame_name, str)
        self._check_type(new_description, str)

        dynamic_frame = {"name": frame_name, "new_name": new_frame_name, "description": new_description}
        req = self._services.edit_dynamic_frame_request(dynamic_frame)
        response = self._services.manage_frame_service.call(req)
        self._check_result_status(response)

    def delete_saved_dynamic_frame(self, frame_name):
        """
        Delete a dynamic frame

        Example: ::

            robot.frames.delete_saved_dynamic_frame("name")

        :param frame_name: name of the frame to remove
        :type frame_name: str
        :return: status, message
        :rtype: (int, str)
        """
        self._check_type(frame_name, str)

        dynamic_frame = {"name": frame_name}
        req = self._services.delete_dynamic_frame_request(dynamic_frame)
        response = self._services.manage_frame_service.call(req)
        self._check_result_status(response)
