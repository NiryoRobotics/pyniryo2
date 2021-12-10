import roslibpy


class SoundServices(object):

    def __init__(self, client):
        self.__client = client

        self.play_sound_user_service = roslibpy.Service(self.__client,
                                                         '/niryo_robot_sound/play_sound_user',
                                                         'niryo_robot_msgs/SoundUserCommand')
                                            
        self.stop_sound_service = roslibpy.Service(self.__client,
                                                         '/niryo_robot_sound/stop_sound',
                                                         'niryo_robot_msgs/StopSound')
            
        self.delete_sound_service = roslibpy.Service(self.__client,
                                                         '/niryo_robot_sound/delete_sound_user',
                                                         'niryo_robot_msgs/DeleteSound')
                                        
        self.set_sound_volume_service = roslibpy.Service(self.__client,
                                                         '/niryo_robot_sound/set_volume',
                                                         'niryo_robot_msgs/SetInt')

        self.import_sound_service = roslibpy.Service(self.__client,
                                                         '/niryo_robot_sound/send_sound',
                                                         'niryo_robot_msgs/SendUserSound')

        
    @staticmethod
    def play_sound_user_request(sound_name):
        """

        :param sound_name:
        :type sound_name: string
        :return:
        :rtype: ServiceRequest
        """
        return roslibpy.ServiceRequest({"sound_name": sound_name})

    @staticmethod
    def delete_sound_request(sound_name):
        """

        :param sound_name:
        :type sound_name: string
        :return:
        :rtype: ServiceRequest
        """
        return roslibpy.ServiceRequest({"sound_name": sound_name})

    @staticmethod
    def set_sound_volume_request(value):
        """

        :param value:
        :type value: int8
        :return:
        :rtype: ServiceRequest
        """
        return roslibpy.ServiceRequest({"value": value})

    @staticmethod
    def import_sound_request(sound_name, sound_data):
        """

        :param sound_name:
        :type sound_name: string
        :param sound_data:
        :type sound_data: string
        :return:
        :rtype: ServiceRequest
        """
        return roslibpy.ServiceRequest(
            {"sound_name": sound_name, "sound_data": sound_data})