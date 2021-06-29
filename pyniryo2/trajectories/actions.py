import roslibpy.actionlib


class TrajectoriesActions(object):

    def __init__(self, client):
        self.__client = client

        self.trajectory_action = None
        self.trajectory_action = roslibpy.actionlib.ActionClient(self.__client,
                                                      '/niryo_robot_arm_commander/robot_action/',
                                                      'niryo_robot_arm_commander/RobotMoveAction')

    def __del__(self):
        if self.trajectory_action:
            self.trajectory_action.dispose()