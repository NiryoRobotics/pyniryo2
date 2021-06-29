import roslibpy

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
    def trajectory_dict_to_list(traj_dict):
        print traj_dict
        traj_list = []
        for pose_dict in traj_dict:
            pose_list = TrajectoriesServices.pose_quat_dict_to_list(pose_dict)
            traj_list.append(pose_list)
        return traj_list

    @staticmethod
    def pose_quat_dict_to_list(pose_dict):
        return [pose_dict["position"]["x"], pose_dict["position"]["y"], pose_dict["position"]["z"],
                pose_dict["orientation"]["x"], pose_dict["orientation"]["y"], pose_dict["orientation"]["z"], pose_dict["orientation"]["w"]]
