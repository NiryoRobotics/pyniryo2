import roslibpy

from pyniryo2.io.enums import PinID


class IOServices(object):

    def __init__(self, client):
        self.__client = client

        self.set_digital_io_mode_service = roslibpy.Service(self.__client,
                                                            '/niryo_robot_rpi/set_digital_io_mode',
                                                            'niryo_robot_rpi/SetIOMode')

        self.set_digital_io_state_service = roslibpy.Service(self.__client,
                                                             '/niryo_robot_rpi/set_digital_io',
                                                             'niryo_robot_rpi/SetDigitalIO')

        self.get_digital_io_service = roslibpy.Service(self.__client,
                                                       '/niryo_robot_rpi/get_digital_io',
                                                       'niryo_robot_rpi/GetDigitalIO')

        self.set_analog_io_state_service = roslibpy.Service(self.__client,
                                                             '/niryo_robot_rpi/set_analog_io',
                                                             'niryo_robot_rpi/SetAnalogIO')

        self.get_analog_io_service = roslibpy.Service(self.__client,
                                                       '/niryo_robot_rpi/set_digital_io',
                                                       'niryo_robot_rpi/GetAnalogIO')

    @staticmethod
    def set_io_mode_request(pin, value):
        pin_name = pin.value if isinstance(pin, PinID) else pin
        return roslibpy.ServiceRequest({"pin": pin_name, "value": value.value})

    @staticmethod
    def set_io_state_request(pin, value):
        pin_name = pin.value if isinstance(pin, PinID) else pin
        return roslibpy.ServiceRequest({"pin": pin_name, "value": value.value})

    @staticmethod
    def get_io_request(pin):
        pin_name = pin.value if isinstance(pin, PinID) else pin
        return roslibpy.ServiceRequest({"pin": pin_name})
