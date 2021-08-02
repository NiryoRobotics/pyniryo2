#!/usr/bin/env python
import unittest
import roslibpy
import time
from threading import Event
import numpy as np

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.led_ring.led_ring import LedRing
from pyniryo2.led_ring.enums import AnimationMode, LedMode
from pyniryo2.arm.arm import Arm
# from pyniryo2.objects import PoseObject

robot_ip_address = "192.168.1.52"
port = 9090

test_order = ["test_creation_delete_trajectory",
              "test_save_trajectory_type",
              "test_execute_trajectory",
              "test_execute_trajectory_type",
              ]

WHITE = [255.0, 255.0, 255.0]
GREEN = [0.0, 255.0, 0.0]
NONE = [0.0, 0.0, 0.0] # or [51.0, 51.0, 51.0] if simu

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = roslibpy.Ros(host=robot_ip_address, port=port)
        cls.client.run()
        cls.led_ring = LedRing(cls.client)
        cls.arm = Arm(cls.client)

    @classmethod
    def tearDownClass(cls):
        # cls.arm.go_to_sleep()
        cls.led_ring.led_ring_turn_off()
        cls.arm.go_to_sleep()
        cls.client.terminate()

    def assertHasAttr(self, obj, intendedAttr):
        testBool = hasattr(obj, intendedAttr)
        self.assertTrue(testBool, msg='obj lacking an attribute. obj: %s, intendedAttr: %s' % (obj, intendedAttr))


# noinspection PyTypeChecker
class TestLedRing(BaseTest):
    neutral_pose = [0.2, 0.0, 0.4, 0., 0., 0.]

    def go_to_neutral_pose(self):
        self.assertIsNone(self.arm.move_pose(self.neutral_pose))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), self.neutral_pose)

    def test_led_ring_status_obj(self, led_ring_status):
        self.assertHasAttr(led_ring_status, "led_mode")
        self.assertHasAttr(led_ring_status, "animation_mode")
        self.assertHasAttr(led_ring_status, "animation_color")

    def test_led_ring_color_obj(self, led_ring_color_state):
        self.assertIsInstance(led_ring_color_state, list)
        self.assertEqual(len(led_ring_color_state), 30)

    # - Test functions

    def test_led_display_robot_status(self): # TODO : we need to access/publish on robot status to check every status
        # Launch first calibration
        self.assertTrue(self.arm.calibrate_auto())
        self.go_to_neutral_pose()

        # - Test Led Ring display learning mode
        self.arm.learning_mode = True

        led_ring_status = self.led_ring.get_led_ring_status()
        self.test_led_ring_status(led_ring_status)
        self.assertEqual(led_ring_status.led_mode, LedMode.ROBOT_STATUS)
        self.assertEqual(led_ring_status.animation_mode, AnimationMode.SOLID)

        led_ring_color_state = self.led_ring.get_led_ring_colors()
        self.test_led_ring_color_obj(led_ring_color_state)
        for i in range(30):
            self.assertEqual(led_ring_color_state[i], WHITE)
        
        self.assertIsNone(time.sleep(1))


        # - Test Led Ring display standby
        self.arm.learning_mode = False
        led_ring_status = self.led_ring.get_led_ring_status()
        self.test_led_ring_status(led_ring_status)
        self.assertEqual(led_ring_status.led_mode, LedMode.ROBOT_STATUS)
        self.assertEqual(led_ring_status.animation_mode, AnimationMode.SOLID)

        led_ring_color_state = self.led_ring.get_led_ring_colors()
        self.test_led_ring_color_obj(led_ring_color_state)
        for i in range(30):
            self.assertEqual(led_ring_color_state[i], GREEN)

        self.assertIsNone(time.sleep(1))


        # - Test Led Ring display moving # TODO : thread for the movement and thread to check color ? OR use a callback
        # Led Ring must be flashing green
        joints = [0., 0., 0., 0., 0., 0.]
        def check_move_color(color):
            self.test_led_ring_color_obj(color)
            for i in range(30):
                self.assertTrue(color[i] == GREEN or color[i] == NONE)

        def check_move_status(status):
            self.test_led_ring_status(led_ring_status)
            self.assertEqual(led_ring_status.led_mode, LedMode.ROBOT_STATUS)
            self.assertEqual(led_ring_status.animation_mode, AnimationMode.FLASHING)

        def move_finished(_): #TEST
            self.led_ring.led_ring_colors.unsubscribe()
            self.led_ring.get_led_ring_status.unsubscribe()

        self.led_ring.led_ring_colors.subscribe(check_move_color)
        self.led_ring.get_led_ring_status.subscribe(check_move_status)
        self.assertIsNone(self.arm.move_joints(joints, callback = move_finished))
        # self.led_ring.led_ring_colors.unsubscribe()
        # self.led_ring.get_led_ring_status.unsubscribe()


    def test_led_controlled_user(self): # TODO : activate autonomous mode first
        # - NONE
        self.assertIsNone(self.led_ring.led_ring_turn_off()) # TODO: test with 'wait'
        led_ring_status = self.led_ring.get_led_ring_status()
        self.test_led_ring_status(led_ring_status)
        self.assertEqual(led_ring_status.led_mode, LedMode.USER)
        self.assertEqual(led_ring_status.animation_mode, AnimationMode.NONE)

        led_ring_color_state = self.led_ring.get_led_ring_colors()
        self.test_led_ring_color_obj(led_ring_color_state)
        for i in range(30):
            self.assertEqual(led_ring_color_state[i], NONE)

        self.assertIsNone(time.sleep(1))

        # - SOLID
        color_solid = [178.0, 189.0, 230.0]
        self.assertIsNone(self.led_ring.led_ring_solid(color_solid))
        led_ring_status = self.led_ring.get_led_ring_status()
        self.test_led_ring_status(led_ring_status)
        self.assertEqual(led_ring_status.led_mode, LedMode.USER)
        self.assertEqual(led_ring_status.animation_mode, AnimationMode.SOLID)

        led_ring_color_state = self.led_ring.get_led_ring_colors()
        self.test_led_ring_color_obj(led_ring_color_state)
        for i in range(30):
            self.assertEqual(led_ring_color_state[i], color_solid)

        # - Flashing
        color_flashing = [0.0, 255.0, 164.0]
        def check_flash(color):
            for i in range(30):
                self.assertTrue(color[i] == color_flashing or color[i] == NONE)
            
        self.led_ring.led_ring_colors.subscribe(check_flash)
        self.assertIsNone(self.led_ring.led_ring_flash(color_flashing, wait = True, iterations = 10)) # TODO: test with different args
        self.led_ring.led_ring_colors.unsubscribe()



def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestLedRing(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
