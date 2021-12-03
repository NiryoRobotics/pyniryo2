#!/usr/bin/env python
import unittest
import roslibpy
import time

from pyniryo2.exceptions import RobotCommandException

from pyniryo2.sound.sound import Sound

robot_ip_address = "127.0.0.1"
port = 9090

test_order = ["test_sound_run",
              "test_bad_params_errors"]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = roslibpy.Ros(host=robot_ip_address, port=port)
        cls.client.run()
        cls.sound = Sound(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.terminate()


# noinspection PyTypeChecker
class TestSound(BaseTest):
    def test_sound_run(self):
        sound_name_dic = self.sound.get_sound_user()
        self.sound.play_sound_user(str(sound_name_dic["sound_object"][0]["name"]))
        self.assertIsInstance(self.sound.get_sound_user_state(), bool)
        self.assertFalse(self.sound.get_sound_user_state())
        self.assertIsNone(time.sleep(1))

        self.assertIsInstance(self.sound.get_sound_volume(), int)
        self.sound.set_sound_volume(0)
        self.assertEqual(self.sound.get_sound_volume(), 0)
        self.sound.set_sound_volume(150)
        self.assertEqual(self.sound.get_sound_volume(), 100)
        self.sound.set_sound_volume(-50)
        self.assertEqual(self.sound.get_sound_volume(), 0)
        self.assertIsNone(time.sleep(1))

        self.assertIsInstance(self.sound.get_sound_user(), dict)
        sound_name_dic = self.sound.get_sound_user()

        self.assertIsInstance(sound_name_dic["sound_object"][0]["name"], unicode)
        self.assertIsInstance(sound_name_dic["sound_object"][0]["duration"], float)
        self.assertEqual(str(sound_name_dic["sound_object"][0]["name"]), "botw_item.wav")
        number_sounds = len(sound_name_dic["sound_object"])
        self.assertIsNone(time.sleep(1))

        self.sound.delete_sound_user(str(sound_name_dic["sound_object"][0]["name"]))
        sound_name_dic = self.sound.get_sound_user()
        self.assertEqual(len(sound_name_dic["sound_object"]), number_sounds-1)
        self.assertIsNone(time.sleep(1))

    def test_bad_params_errors(self):
        with self.assertRaises(RobotCommandException):
            self.sound.play_sound_user(2)
        
        with self.assertRaises(RobotCommandException):
            self.sound.set_sound_volume("a")

        with self.assertRaises(RobotCommandException):
            self.sound.delete_sound_user(4)

def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestSound(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
