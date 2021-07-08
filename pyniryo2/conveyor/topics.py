from collections import namedtuple

from pyniryo2.niryo_topic import NiryoTopic

ConveyorInfo = namedtuple("ConveyorInfo", ['conveyor_id', 'connection_state', 'running', 'speed', 'direction'])

class ConveyorTopics(object):

    def __init__(self, client):
        self.__client = client

        self.conveyor_feedback_topic = NiryoTopic(self.__client,
                                        '/niryo_robot/conveyor/feedback',
                                        'conveyor_interface/ConveyorFeedbackArray',
                                        conveyor_feedback_topic_conversion)


def conveyor_feedback_topic_conversion(msg):
    return [ConveyorInfo(conveyor_id=conveyor['conveyor_id'], 
                    connection_state=conveyor['connection_state'], 
                    running=conveyor['running'], 
                    speed=conveyor['speed'], 
                    direction=conveyor['direction']) for conveyor in msg['conveyors']]
