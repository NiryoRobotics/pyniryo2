from pyniryo2.niryo_topic import NiryoTopic
from pyniryo2.led_ring.objects import LedRingStatusObject, LedRingStateObject
# from pyniryo2.objects import PoseObject


class LedRingTopics(object):

    def __init__(self, client):
        self.__client = client

        self.led_ring_status_topic = NiryoTopic(self.__client,
                                             '/niryo_robot_led_ring/led_ring_status',
                                             'niryo_robot_led_ring/LedRingStatus',
                                             led_status_topic_conversion)

        self.led_ring_state_topic = NiryoTopic(self.__client,
                                            '/niryo_robot_led_ring/led_ring_current_state',
                                            'niryo_robot_led_ring/LedRingCurrentState',
                                            led_state_topic_conversion)



def led_status_topic_conversion(msg):
    led_status = LedRingStatusObject()
    led_status.init_from_message(msg)
    return led_status

def led_state_topic_conversion(msg):
    led_state = LedRingStateObject()
    led_state.init_from_message(msg)
    return led_state.led_state
