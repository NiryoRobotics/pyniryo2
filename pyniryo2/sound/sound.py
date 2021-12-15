# Communication imports
from pyniryo2.robot_commander import RobotCommander

from .services import SoundServices
from .topics import SoundTopics
from .enums import Language


def check_ned2_version(func):
    """
    Decorator that check the robot version
    """

    def wrap(*args, **kwargs):
        robot_instance = args[0]
        if robot_instance.client.hardware_version != 'ned2':
            raise Exception("Error Code : BAD_HARDWARE_VERSION\n"
                            "Message : Wrong robot hardware version, feature only available on Ned2")

        return func(*args, **kwargs)

    return wrap


class Sound(RobotCommander):
    # --- Public functions --- #
    def __init__(self, client):
        super(Sound, self).__init__(client)

        if self._client.hardware_version == 'ned2':
            self._services = SoundServices(self._client)
            self._topics = SoundTopics(self._client)
        else:
            self._services = None
            self._topics = None

    def __call__(self, *args, **kwargs):
        self.play(*args, **kwargs)

    @check_ned2_version
    @property
    def sounds(self):
        """
        Returns the list of available sounds in the robot

        Examples: ::

            sounds_list = sound.sounds

        :return: Returns the list of available sounds in the robot
        :rtype: list[str]
        """
        return list(self._topics.sound_database_topic().values())

    @check_ned2_version
    def get_sounds(self):
        """
        Returns the list of available sounds in the robot

        Examples: ::

            sounds_list = sound.get_sounds()

        :return: Returns the list of available sounds in the robot
        :rtype: list[str]
        """
        return self.sounds

    @check_ned2_version
    def get_sound_duration(self, sound_name):
        """
        Get the duration of a sound in seconds

        Examples: ::

            sound_name = sound.get_sounds()[0]
            sound_duration = sound.get_sound_duration(sound_name)
            sound_duration = sound.get_sound_duration('test_sound.mp3')

        :return: Returns the duration of a sound in seconds
        :rtype: float
        """
        sounds = self._topics.sound_database_topic()
        self._check_dict_belonging(sound_name, sounds)
        return sounds[sound_name]

    @check_ned2_version
    def play(self, sound_name, wait_end=False, start_time_sec=0, end_time_sec=0):
        """
        Play a sound that as already been imported by the user on the robot. 

        Example: ::

            # If you know that the sound test_sound.wav is already imported on the robot
            sound.play_sound_user("test_sound.wav")

            # If you want to play the first sound of the ones that are already on the robot without knowing its name
            sound_name = sound.get_sounds()[0]
            sound_duration = sound.play(sound_name)

            # Waits until the sound has been fully played
            sound_duration = sound.play(sound_name, wait_end=True)

            #  Doesn't wait until the sound has been fully played
            sound_duration = sound.play(sound_name, wait_end=False)

            # Plays sound from 1.1 seconds from start to 4.3 seconds from start
            sound_duration = sound.play(sound_name, start_time_sec=1.1, end_time_sec=4.3)


        :param: sound_name: Name of the sound that will be played
        :type sound_name: str
        :param wait_end: wait for the end of the sound before exiting the function
        :type wait_end: bool
        :param start_time_sec: start the sound from this value in seconds
        :type start_time_sec: float
        :param end_time_sec: end the sound at this value in seconds
        :type end_time_sec: float
        :rtype: None
        """
        self._check_instance(sound_name, str)
        req = self._services.play_sound_service(sound_name, start_time_sec, end_time_sec, wait_end)
        resp = self._services.play_sound_service.call(req)
        self._check_result_status(resp)

    @check_ned2_version
    def stop_sound(self):
        """
        Stop a sound being played. It will get automatically the name of the sound being played and stop it. 

        Example: ::

            self.sound.stop_sound()

        :rtype: None
        """
        resp = self._services.stop_sound_service.call()
        self._check_result_status(resp)

    @check_ned2_version
    @property
    def sound_state(self):
        """
        Returns the sound state client which can be used synchronously or asynchronously
        to obtain the current played sound.

        Examples: ::

            # Get last value
            sound.sound_state()
            sound.sound_state.value

            # Subscribe a callback
            def sound_callback(sound_name):
                print sound_name

            sound.sound_state.subscribe(sound_callback)
            sound.sound_state.unsubscribe()

        :return: sound state topic instance
        :rtype: NiryoTopic
        """
        return self._topics.current_sound_topic

    @check_ned2_version
    @property
    def volume(self):
        """
        Returns the volume state client which can be used synchronously or asynchronously
        to obtain the current volume.

        Examples: ::

            # Get last value
            sound.volume()
            sound.volume.value

            # Subscribe a callback
            def volume_callback(value):
                print value

            sound.volume.subscribe(volume_callback)
            sound.volume.unsubscribe()

        :return: volume topic instance
        :rtype: NiryoTopic
        """
        return self._topics.volume_topic

    @check_ned2_version
    @property
    def get_volume(self):
        """
        Returns the volume of the robot. The sound can be set between 0 (sound off) and 100 (sound max)

        Examples: ::

            # Get the volume of the sound
            sound.get_sound_volume()

        :return: int8 corresponding to the volume (0: sound off, 100: sound max)
        :rtype: int8
        """
        return self._topics.volume_topic()

    @check_ned2_version
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
        :type sound_volume: int8
        :rtype: None
        """
        req = self._services.set_sound_volume_request(sound_volume)
        resp = self._services.set_sound_volume_service.call(req)
        self._check_result_status(resp)

    @check_ned2_version
    def delete_sound_user(self, sound_name):
        """
        Delete a sound imported on the robot

        Example: ::

            self.sound.delete_sound_user("test_sound.wav")


        :param sound_name: For example, test.wav
        :type sound_name: string
        :rtype: None
        """
        req = self._services.delete_sound_request(sound_name)
        resp = self._services.manage_sound_service.call(req)
        self._check_result_status(resp)

    @check_ned2_version
    def import_sound(self, sound_name, sound_data):
        """
        Import a sound on the RaspberryPi of the robot. To do that,
        you will need the encoded data from a wav or mp3 sound.
        It is preferable to put the encoded data from the sound on a text file and directly read it from this file.
        You also need to give the name of the sound you want to import.

        Example: ::

            sound_name = "test_import_sound.wav"
            with open(sound_name, 'r') as f:
                sound_data = f.read()
            sound.import_sound(sound_name, sound_data)

        :param sound_name: For example, test.wav
        :type sound_name: string
        :param sound_data: encoded data from a sound (type can be wav or mp3)
        :type sound_data: string
        :rtype: None
        """
        req = self._services.import_sound_request(sound_name, sound_data)
        resp = self._services.manage_sound_service.call(req)
        self._check_result_status(resp)

    @check_ned2_version
    def say(self, text, language=Language.ENGLISH):
        """
        Use gtts (Google Text To Speech) to interpret a string as sound
        Languages available are:
            - English: Language. ENGLISH
            - French: Language.FRENCH
            - Spanish: Language.SPANISH
            - Mandarin: Language.MANDARIN
            - Portuguese: Language.PORTUGUESE

        Example ::

            robot.say("Hello", Language.ENGLISH)
            robot.say("Bonjour", Language.FRENCH)
            robot.say("Hola", Language.SPANISH)


        :param text: Text that needs to be spoken < 100 char
        :type text: string
        :param language: language of the text
        :type language: Language
        :rtype: None
        """
        self._check_enum_belonging(language, Language)
        self._check_type(text, str)

        req = self._services.tts_request(text, language)
        resp = self._services.tts_service.call(req)
        self._check_result_status(resp)
