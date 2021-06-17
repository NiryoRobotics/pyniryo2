import roslibpy
from pyniryo2.vision.enums import ManageWorkspace

class VisionServices(object):

    def __init__(self, client):
        self.__client = client

        self.get_target_pose_service = roslibpy.Service(self.__client,
                                                        '/niryo_robot_poses_handlers/get_target_pose',
                                                        'niryo_robot_vision/GetTargetPose')

        self.obj_detection_rel_service = roslibpy.Service(self.__client,
                                                          '/niryo_robot_vision/obj_detection_rel',
                                                          'niryo_robot_vision/ObjDetection')

        self.manage_workspace_service = roslibpy.Service(self.__client,
                                                         '/niryo_robot_poses_handlers/manage_workspace',
                                                         'niryo_robot_poses_handlers/ManageWorkspace')

        self.get_workspace_poses_service = roslibpy.Service(self.__client,
                                                            '/niryo_robot_poses_handlers/get_workspace_poses',
                                                            'niryo_robot_poses_handlers/GetWorkspaceRobotPoses')

        self.get_workspace_ratio_service = roslibpy.Service(self.__client,
                                                            '/niryo_robot_poses_handlers/get_workspace_ratio',
                                                            'niryo_robot_msgs/GetWorkspaceRatio')

        self.get_workspace_list_service = roslibpy.Service(self.__client,
                                                           '/niryo_robot_poses_handlers/get_workspace_list',
                                                           'niryo_robot_msgs/GetNameDescriptionList')

    @staticmethod
    def get_trigger_request():
        return roslibpy.ServiceRequest()

    @staticmethod
    def get_target_pose_service_request(workspace, height_offset, x_rel, y_rel, yaw_rel):
        return roslibpy.ServiceRequest(
            {"workspace": workspace, "height_offset": height_offset, "x_rel": x_rel, "y_rel": y_rel,
             "yaw_rel": yaw_rel})

    @staticmethod
    def obj_detection_rel_service_request(obj_type, obj_color, workspace_ratio, ret_image=False):
        return roslibpy.ServiceRequest(
            {"obj_type": obj_type, "obj_color": obj_color, "workspace_ratio": workspace_ratio, "ret_image": ret_image})

    @staticmethod
    def manage_workspace_service_request(cmd, workspace):
        if not isinstance(cmd, ManageWorkspace):
            raise TypeError
        return roslibpy.ServiceRequest({"cmd": cmd.value, "workspace": workspace})

    @staticmethod
    def get_workspace_poses_service_request(workspace_name):
        return roslibpy.ServiceRequest({"name": workspace_name})

    @staticmethod
    def get_workspace_ratio_service_request(workspace_name):
        return roslibpy.ServiceRequest({"workspace": workspace_name})

    @staticmethod
    def get_workspace_list_service_request():
        return VisionServices.get_trigger_request()

    @staticmethod
    def pose_dict_to_list(pose_dict):
        return [pose_dict["position"]["x"], pose_dict["position"]["y"], pose_dict["position"]["z"],
                pose_dict["rpy"]["roll"], pose_dict["rpy"]["pitch"], pose_dict["rpy"]["yaw"]]
