import roslibpy
from pyniryo2.io.objects import DigitalPinObject
from pyniryo2.io.enums import PinID, PinMode, PinState


class IOServices(object):

    def __init__(self, client):
        self.__client = client

        self.set_digital_io_mode_service = roslibpy.Service(self.__client,
                                                            '/niryo_robot_rpi/set_digital_io_mode',
                                                            'niryo_robot_rpi/SetDigitalIO')

        self.set_digital_io_state_service = roslibpy.Service(self.__client,
                                                             '/niryo_robot_rpi/set_digital_io_state',
                                                             'niryo_robot_rpi/SetDigitalIO')

        self.get_digital_io_service = roslibpy.Service(self.__client,
                                                       '/niryo_robot_rpi/get_digital_io',
                                                       'niryo_robot_rpi/GetDigitalIO')

    @staticmethod
    def set_digital_io_mode_request(pin, value):
        return roslibpy.ServiceRequest({"pin": pin.value, "value": value.value})

    @staticmethod
    def set_digital_io_state_request(pin, value):
        return roslibpy.ServiceRequest({"pin": pin.value, "value": value.value})

    @staticmethod
    def get_digital_io_request(pin):
        return roslibpy.ServiceRequest({"pin": pin.value})

    @staticmethod
    def get_digital_io_response_to_object(response):
        return DigitalPinObject(PinID(response["pin"]), str(response["name"]), PinMode(response["mode"]),
                                PinState(response["state"]))
