from pyniryo2.niryo_topic import NiryoTopic
from pyniryo2.io.objects import DigitalPinObject
from pyniryo2.io.enums import PinID, PinMode, PinState

class IOTopics(object):

    def __init__(self, client):
        self.__client = client

        self.io_topic = NiryoTopic(self.__client,
                                             '/niryo_robot_rpi/digital_io_state',
                                             'niryo_robot_rpi/DigitalIOState',
                                             digital_io_state_topic_conversion)


def digital_io_state_topic_conversion(msg):
    return [DigitalPinObject(PinID(pin), str(name), PinMode(mode), PinState(state)) for pin, name, mode, state in
            zip(msg["pins"], msg["names"], msg["modes"], msg["states"])]
