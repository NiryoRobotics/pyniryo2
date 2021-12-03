from pyniryo2.niryo_topic import NiryoTopic

from .objects import ConveyorInfo
from .enums import ConveyorID, ConveyorDirection


class ConveyorTopics(object):

    def __init__(self, client):
        self.__client = client

        self.conveyor_feedback_topic = NiryoTopic(self.__client,
                                                  '/niryo_robot/conveyor/feedback',
                                                  'conveyor_interface/ConveyorFeedbackArray',
                                                  conveyor_feedback_topic_conversion)


def conveyor_feedback_topic_conversion(msg):
    return [ConveyorInfo(conveyor_id=ConveyorID(conveyor['conveyor_id']),
                         running=conveyor['running'],
                         speed=conveyor['speed'],
                         direction=ConveyorDirection(conveyor['direction'])) for conveyor in msg['conveyors']]
