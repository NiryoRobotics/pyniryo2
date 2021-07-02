import roslibpy

from .enums import ManageTrajectories

class TrajectoriesServices(object):

    def __init__(self, client):
        self.__client = client

        self.get_trajectory_from_name_service = roslibpy.Service(self.__client,
                                                    '/niryo_robot_poses_handlers/get_trajectory',
                                                    'niryo_robot_poses_handlers/GetTrajectory')

        self.save_delete_trajectory_service = roslibpy.Service(self.__client,
                                                    '/niryo_robot_poses_handlers/manage_trajectory',
                                                    'niryo_robot_poses_handlers/ManageTrajectory')

        self.get_trajectory_list_service = roslibpy.Service(self.__client,
                                                    '/niryo_robot_poses_handlers/get_trajectory_list',
                                                    'niryo_robot_msgs/GetNameDescriptionList')
    @staticmethod
    def get_trajectory_from_name_request(traj_name):
        return roslibpy.ServiceRequest({"name": traj_name})

    @staticmethod
    def save_trajectory_request(name, poses, description=""):
        return roslibpy.ServiceRequest({"cmd": ManageTrajectories.SAVE.value, "name": name, "description": description,
                                        "poses": [TrajectoriesServices.pose_quat_list_to_dict(pose) for pose in poses]})
    @staticmethod
    def delete_trajectory_request(name):
        return roslibpy.ServiceRequest({"cmd": ManageTrajectories.DELETE.value, "name": name})

    @staticmethod
    def get_saved_trajectory_list_request():
        return roslibpy.ServiceRequest()

    @staticmethod
    def get_saved_trajectory_list_response_to_list(response):
        return [str(pose_name) for pose_name in response["name_list"]]

    @staticmethod
    def trajectory_dict_to_list(traj_dict):
        return [TrajectoriesServices.pose_quat_dict_to_list(pose_dict) for pose_dict in traj_dict]

    @staticmethod
    def pose_quat_dict_to_list(pose_dict):
        return [pose_dict["position"][axis] for axis in ["x", "y", "z"]] + \
               [pose_dict["orientation"][axis] for axis in ["x", "y", "z", "w"]]

    @staticmethod
    def pose_quat_list_to_dict(pose_list):
        return {"position": dict(zip(["x", "y", "z"], pose_list[:3])),
                "orientation": dict(zip(["x", "y", "z", "w"], pose_list[3:]))}
