from pyniryo2.niryo_topic import NiryoTopic


class SoundTopics(object):

    def __init__(self, client):
        self.__client = client

        self.sound_user_state_topic = NiryoTopic(self.__client,
                                                  '/niryo_robot_sound/sound_user_state',
                                                  'std_msgs/Bool',
                                                  sound_user_state_conversion)
                            
        self.sound_volume_state_topic = NiryoTopic(self.__client,
                                                  '/niryo_robot_sound/volume_state',
                                                  'std_msgs/Int8',
                                                  sound_volume_state_conversion)
                                    
        self.sound_user_topic = NiryoTopic(self.__client,
                                                  '/niryo_robot_sound/get_user_sounds',
                                                  'niryo_robot_msgs/SoundUser',
                                                  get_user_sounds_conversion)


def sound_user_state_conversion(msg):
    return msg["data"]

def sound_volume_state_conversion(msg):
    return msg["data"]

def get_user_sounds_conversion(msg):
    return msg
