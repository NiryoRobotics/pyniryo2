# Communication imports
from pyniryo2.robot_commander import RobotCommander

from .services import SoundServices
from .topics import SoundTopics


class Sound(RobotCommander):
    # --- Public functions --- #
    def __init__(self, client):
        super(Sound, self).__init__(client)

        self._services = SoundServices(self._client)
        self._topics = SoundTopics(self._client)

    def play_sound_user(self, sound_name):
        """
        Play a sound that as already been imported by the user on the robot. 

        Example: ::

        # If you know that the sound test_sound.wav is already imported on the robot
        self.sound.play_sound_user("test_sound.wav")

        # If you want to play the first sound of the ones that are already on the robot without knowing its name
        sound_name_dic = self.sound.get_sound_user() 
        self.sound.play_sound_user(str(sound_name_dic["sound_object"][0]["name"]))

        :param: sound_name: Name of the sound that will be played
        :type sound_name: str
        :rtype: None
        """
        req = self._services.play_sound_user_request(sound_name)
        resp = self._services.play_sound_user_service.call(req)
        self._check_result_status(resp)
    
    def stop_sound(self):
        """
        Stop a sound being played. It will get automatically the name of the sound being played and stop it. 

        Example: ::
        self.sound.stop_sound()
            
        
        :param sound_name: For example, test.wav
        :type: string
        :rtype: None
        """
        resp = self._services.stop_sound_service.call()
        self._check_result_status(resp)

    def delete_sound_user(self, sound_name):
        """
        Delete a sound imported on the robot

        Example: ::

        # If you know the name of the sound you want to delete 
        self.sound.delete_sound_user("test_sound.wav")

        # If you want to delete the first sound of the ones that are already on the robot without knowing its name
        sound_name_dic = self.sound.get_sound_user()
        self.sound.delete_sound_user(str(sound_name_dic["sound_object"][0]["name"]))
            
        
        :param sound_name: For example, test.wav
        :type sound_name: string
        :rtype: None
        """
        req = self._services.delete_sound_request(sound_name)
        resp = self._services.delete_sound_service.call(req)
        self._check_result_status(resp)

    def set_sound_volume(self, sound_volume):
        """
        Set the volume of the robot. You can set it between 0 and 100 (0: sound off and 100: sound max).
        If you put less than 0, the volume will be set to 0. 
        If you put more than 100, the volume will be set to 100.

        Example: ::

        # Set the volume to 25
        self.sound.set_sound_volume(25)
        self.sound.play_sound_user("test_sound.wav")


        :param sound_volume: Between O and 100 (0 sound off and 100 sound maximum)
        :type sound_name: int8
        :rtype: None
        """
        req = self._services.set_sound_volume_request(sound_volume)
        resp = self._services.set_sound_volume_service.call(req)
        self._check_result_status(resp)

    def import_sound(self, sound_name, sound_data):
        """
        Import a sound on the RaspberryPi of the robot. To do that, you will need the encoded data from a wav or mp3 sound. 
        It is preferable to put the encoded data from the sound on a text file and directly read it from this file.
        You also need to give the name of the sound you want to import. 

        Example: ::

        sound_name = "test_import_sound.wav"
        sound_data = "UklGRlUMAgBXQVZFSlVOSxwAAAAAAAAAAA (...) LQI2b+Inx+RyYOobg+oxVP/" #data encoded from a wav sound
        self.sound.import_sound(sound_name, sound_data)
        
        :param sound_name: For example, test.wav
        :type sound_name: string
        :param sound_data: encoded data from a sound (type can be wav or mp3)
        :type sound_data: string
        :rtype: None
        """
        req = self._services.import_sound_request(sound_name, sound_data)
        resp = self._services.import_sound_service.call(req)
        self._check_result_status(resp)

    @property
    def get_sound_user_state(self):
        """
        Returns the state of a sound. 
        If a sound is being played, the state will be True. If not, the state will be False.
        When the state is True, no other sound can be played before the end. 

        Examples: ::

        # Get the state of the sound 
        self.sound.get_sound_user_state()

        :return: bool (True if a sound is being played, false if not)
        :rtype: bool
        """
        return self._topics.sound_user_state_topic

    @property
    def get_sound_volume(self):
        """
        Returns the volume of the robot. The sound can be set between 0 (sound off) and 100 (sound max)

        Examples: ::

        # Get the volume of the sound 
        self.sound.get_sound_volume()

        :return: int8 corresponding to the volume (0: sound off, 100: sound max)
        :rtype: int8
        """
        return self._topics.sound_volume_state_topic

    @property
    def get_sound_user(self):
        """
        Returns an object with the names and the duration of the sounds on the robot 

        Examples: ::

        # get a dictionary with the sound_name and their duration
        sound_name_dic = self.sound.get_sound_user()

        # Get the name of the first sound on the robot
        str(sound_name_dic["sound_object"][0]["name"])

        # Get the duration of the first sound on the robot
        str(sound_name_dic["sound_object"][0]["duration"])


        :return: SoundUser (name: correspond to the name of the sound, duration: correspond to the duration of the sound)
        :rtype: SoundUser
        """
        return self._topics.sound_user_topic