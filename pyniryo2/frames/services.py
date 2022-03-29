import roslibpy

from .enums import ManageFrames


class FramesServices(object):

    def __init__(self, client):
        self.__client = client

        self.get_frame_from_name_service = roslibpy.Service(self.__client,
                                                            '/niryo_robot_poses_handlers/get_dynamic_frame',
                                                            'niryo_robot_poses_handlers/GetDynamicFrame')

        self.manage_frame_service = roslibpy.Service(self.__client,
                                                     '/niryo_robot_poses_handlers/manage_dynamic_frame',
                                                     'niryo_robot_poses_handlers/ManageDynamicFrame')

        self.get_frame_list_service = roslibpy.Service(self.__client,
                                                       '/niryo_robot_poses_handlers/get_dynamic_frame_list',
                                                       'niryo_robot_msgs/GetNameDescriptionList')

    @staticmethod
    def get_dynamic_frame_from_name_request(frame_name):
        return roslibpy.ServiceRequest({"name": frame_name})

    @staticmethod
    def get_dynamic_frame_from_name_response_to_list(response):
        response = response["dynamic_frame"]
        name = response["name"]
        description = response["description"]
        position = [response["position"]["x"], response["position"]["y"], response["position"]["z"]]
        orientation = [response["rpy"]["roll"], response["rpy"]["pitch"], response["rpy"]["yaw"]]
        return [name, description, position, orientation]

    @staticmethod
    def save_dynamic_frame_from_points_request(frame_name, description, points_list):
        dynamic_frame = {"name": frame_name, "description": description, "points": points_list}
        return roslibpy.ServiceRequest(
            {"cmd": ManageFrames.SAVE_WITH_POINTS.value, "dynamic_frame": dynamic_frame})

    @staticmethod
    def edit_dynamic_frame_request(frame_name, new_frame_name, new_description):
        dynamic_frame = {"name": frame_name, "new_name": new_frame_name, "description": new_description}
        return roslibpy.ServiceRequest({"cmd": ManageFrames.EDIT.value, "dynamic_frame": dynamic_frame})

    @staticmethod
    def delete_dynamic_frame_request(frame_name):
        return roslibpy.ServiceRequest({"cmd": ManageFrames.DELETE.value, "dynamic_frame": {"name": frame_name}})

    @staticmethod
    def get_saved_dynamic_frame_list_request():
        return roslibpy.ServiceRequest()

    @staticmethod
    def get_saved_dynamic_frame_list_response_to_list(response):
        name = [str(pose_name) for pose_name in response["name_list"]]
        desc = [str(desc) for desc in response["description_list"]]
        return name, desc
