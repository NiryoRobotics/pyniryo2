import roslibpy
from pyniryo2.conveyor.enums import ConveyorStatus


class ConveyorServices(object):

    def __init__(self, client):
        self.__client = client

        self.ping_and_set_conveyor_service = roslibpy.Service(self.__client,
                                                            '/niryo_robot/conveyor/ping_and_set_conveyor',
                                                            'conveyor_interface/SetConveyor')

        self.control_conveyor_service = roslibpy.Service(self.__client,
                                                            '/niryo_robot/conveyor/control_conveyor',
                                                            'conveyor_interface/ControlConveyor')
    
    
    @staticmethod
    def get_ping_and_set_conveyor_request(cmd_type):
        return roslibpy.ServiceRequest({"cmd": cmd_type})

    @staticmethod
    def unset_conveyor_request(conveyor_id):
        return roslibpy.ServiceRequest({"cmd": ConveyorStatus.REMOVE.value, "id": conveyor_id})
    
    @staticmethod
    def control_conveyor_request(conveyor_id, control_on, speed, direction):
        return roslibpy.ServiceRequest({"id": conveyor_id, "control_on": control_on, "speed": speed, "direction": direction})