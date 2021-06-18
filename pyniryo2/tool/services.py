import roslibpy
from pyniryo2.tool.enums import ToolID


class ToolServices(object):

    def __init__(self, client):
        self.__client = client

        self.update_tool_service = roslibpy.Service(self.__client,
                                                    '/niryo_robot_tools_commander/update_tool',
                                                    'niryo_robot_msgs/Trigger')

        self.equip_electromagnet_service = roslibpy.Service(self.__client,
                                                            '/niryo_robot_tools_commander/equip_electromagnet',
                                                            'niryo_robot_msgs/SetInt')

    @staticmethod
    def get_trigger_request():
        return roslibpy.ServiceRequest()

    @staticmethod
    def equip_electromagnet_service_request(id_=ToolID.ELECTROMAGNET_1):
        return roslibpy.ServiceRequest({"value": id_.value})
