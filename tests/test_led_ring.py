#!/usr/bin/env python
import unittest
import roslibpy
import time
import random

from pyniryo2.led_ring import AnimationMode, LedMode
from pyniryo2.led_ring import LedRing
from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_ros import NiryoRos

from pyniryo2.enums import RobotErrors
from pyniryo2.arm.arm import Arm

robot_ip_address = "192.168.1.92"
port = 9090

test_order = [
    "test_ledring",
]

WHITE = [255.0, 255.0, 255.0]
GREEN = [0.0, 255.0, 0.0]
NONE = [0.0, 0.0, 0.0]
RED = [255.0, 0.0, 0.0]
YELLOW = [255.0, 255.0, 0.0]
BLUE = [0.0, 0.0, 255.0]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = NiryoRos(ip_address=robot_ip_address, port=port)
        time.sleep(20)
        cls.arm = Arm(cls.client)
        cls.led_ring = LedRing(cls.client)

        print("-- Connected --")

    @classmethod
    def tearDownClass(cls):
        cls.led_ring.turn_off()
        cls.arm.go_to_sleep()
        cls.arm.learning_mode = True
        cls.client.terminate()


# noinspection PyTypeChecker
class TestLedRing(BaseTest):
    neutral_pose = [0.2, 0.0, 0.4, 0., 0., 0.]
    nb_leds = 30

    def go_to_neutral_pose(self):
        self.assertIsNone(self.arm.move_pose(self.neutral_pose))

    def test_ledring(self):
        self.assertEqual(self.led_ring.get_status().mode, LedMode.USER)

        self.test_solid()
        self.test_set_led()
        self.test_custom()
        self.test_alternate()

        self.test_classic_animation(self.led_ring.flash, AnimationMode.FLASHING)
        self.test_classic_animation(self.led_ring.chase, AnimationMode.CHASE)
        self.test_classic_animation(self.led_ring.go_up, AnimationMode.GO_UP)
        self.test_classic_animation(self.led_ring.go_up_down, AnimationMode.GO_UP_AND_DOWN)
        self.test_classic_animation(self.led_ring.breath, AnimationMode.BREATH)
        self.test_classic_animation(self.led_ring.snake, AnimationMode.SNAKE)

        self.test_rainbow_animation(self.led_ring.rainbow, AnimationMode.RAINBOW)
        self.test_rainbow_animation(self.led_ring.rainbow_cycle, AnimationMode.RAINBOW_CYLE)
        self.test_rainbow_animation(self.led_ring.rainbow_chase, AnimationMode.RAINBOW_CHASE)

        self.assertIsNotNone(self.led_ring.turn_off())

    def test_classic_animation(self, function, animation):
        color = [random.randint(0, 255) for _ in range(3)]
        duration = random.uniform(1, 3)
        iterations = random.randint(1, 10)
        period = duration / iterations

        start_time = time.time()
        self.assertIsNone(function(color, period=period, iterations=iterations, wait=True))
        self.assertTrue(0 <= time.time() - start_time - duration < 1)
        self.assertIsNone(self.led_ring.turn_off())

        start_time = time.time()
        self.assertIsNone(function(color, period=period, iterations=iterations, wait=False))
        self.assertTrue(time.time() - start_time < 1)
        time.sleep(0.2)
        status = self.led_ring.get_status()
        self.assertEqual(status.mode, LedMode.USER)
        self.assertEqual(status.animation, animation)
        self.assertEqual([status.r, status.g, status.b], color)
        self.assertIsNone(self.led_ring.turn_off())

        start_time = time.time()

        def animation_callback(resp):
            self.assertTrue(0 <= time.time() - start_time - duration < 1)
            self.assertEqual(resp['status'], RobotErrors.SUCCESS.value)

        self.assertIsNone(function(color, period=period, iterations=iterations, wait=True, callback=animation_callback))
        self.assertIsNone(self.led_ring.turn_off())

        with self.assertRaises(RobotCommandException):
            function(color, period=period, iterations=1.5, wait=True)

        with self.assertRaises(RobotCommandException):
            function(color, period=period, iterations=1, wait=50)

        with self.assertRaises(RobotCommandException):
            function([], period=period, iterations=1, wait=50)

        with self.assertRaises(RobotCommandException):
            function(10, period=period, iterations=1, wait=50)

    def test_rainbow_animation(self, function, animation):
        duration = random.uniform(2, 5)
        iterations = random.randint(1, 3)
        period = duration / iterations

        start_time = time.time()
        self.assertIsNone(function(period=period, iterations=iterations, wait=True))
        self.assertTrue(0 <= time.time() - start_time - duration < 1)
        self.assertIsNone(self.led_ring.turn_off())

        start_time = time.time()
        self.assertIsNone(function(period=period, iterations=iterations, wait=False))
        self.assertTrue(time.time() - start_time < 1)
        time.sleep(0.2)
        status = self.led_ring.get_status()
        self.assertEqual(status.mode, LedMode.USER)
        self.assertEqual(status.animation, animation)
        self.assertIsNone(self.led_ring.turn_off())

        start_time = time.time()

        def animation_callback(resp):
            self.assertTrue(0 <= time.time() - start_time - duration < 1)
            self.assertEqual(resp['status'], RobotErrors.SUCCESS.value)

        self.assertIsNone(function(period=period, iterations=iterations, wait=True, callback=animation_callback))
        self.assertIsNone(self.led_ring.turn_off())

        with self.assertRaises(RobotCommandException):
            function(period=period, iterations=1.5, wait=True)

        with self.assertRaises(RobotCommandException):
            function(period=period, iterations=1, wait=50)

    def test_alternate(self):
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(3)]
        duration = random.uniform(1, 3)
        iterations = random.randint(1, 10)
        period = duration / iterations

        start_time = time.time()
        self.assertIsNone(self.led_ring.alternate(colors, period=period, iterations=iterations, wait=True))
        self.assertTrue(0 <= time.time() - start_time - duration < 1)
        self.assertIsNone(self.led_ring.turn_off())

        start_time = time.time()
        self.assertIsNone(self.led_ring.alternate(colors, period=period, iterations=iterations, wait=False))
        self.assertTrue(time.time() - start_time < 1)
        time.sleep(0.2)
        status = self.led_ring.get_status()
        self.assertEqual(status.mode, LedMode.USER)
        self.assertEqual(status.animation, AnimationMode.ALTERNATE)
        self.assertTrue([status.r, status.g, status.b] in colors)
        self.assertIsNone(self.led_ring.turn_off())

        start_time = time.time()

        def animation_callback(resp):
            self.assertTrue(0 <= time.time() - start_time - duration < 1)
            self.assertEqual(resp['status'], RobotErrors.SUCCESS.value)

        self.assertIsNone(self.led_ring.alternate(colors, period=period, iterations=iterations, wait=True,
                                                  callback=animation_callback))
        self.assertIsNone(self.led_ring.turn_off())

        with self.assertRaises(RobotCommandException):
            self.led_ring.alternate(colors, period=period, iterations=1.5, wait=True)

        with self.assertRaises(RobotCommandException):
            self.led_ring.alternate(colors, period=period, iterations=1, wait=50)

        with self.assertRaises(RobotCommandException):
            self.led_ring.alternate([], period=period, iterations=1, wait=50)

        with self.assertRaises(RobotCommandException):
            self.led_ring.alternate(10, period=period, iterations=1, wait=50)

    def test_wipe(self):
        color = [random.randint(0, 255) for _ in range(3)]
        period = random.uniform(1, 4)

        start_time = time.time()
        self.assertIsNotNone(self.led_ring.wipe(color, period=period, wait=True))
        self.assertTrue(0 <= time.time() - start_time - period < 1)
        self.assertIsNone(self.led_ring.turn_off())

        start_time = time.time()
        self.assertIsNone(self.led_ring.alternate(color, period=period, wait=False))
        self.assertTrue(time.time() - start_time < 1)
        time.sleep(0.2)
        status = self.led_ring.get_status()
        self.assertEqual(status.mode, LedMode.USER)
        self.assertEqual(status.animation, AnimationMode.COLOR_WIPE)
        self.assertTrue([status.r, status.g, status.b] == color)
        self.assertIsNone(self.led_ring.turn_off())

        start_time = time.time()

        def animation_callback(resp):
            self.assertTrue(0 <= time.time() - start_time - period < 1)
            self.assertEqual(resp['status'], RobotErrors.SUCCESS.value)

        self.assertIsNone(self.led_ring.alternate(color, period=period, wait=True, callback=animation_callback))
        self.assertIsNone(self.led_ring.turn_off())

        with self.assertRaises(RobotCommandException):
            self.led_ring.alternate(color, period=[], wait=True)

        with self.assertRaises(RobotCommandException):
            self.led_ring.alternate(color, period=period, wait=50)

        with self.assertRaises(RobotCommandException):
            self.led_ring.alternate([], period=period, iterations=1, wait=50)

        with self.assertRaises(RobotCommandException):
            self.led_ring.alternate(10, period=period, iterations=1, wait=50)

    def test_set_led(self):
        for led_id in range(30):
            self.assertIsNotNone(self.led_ring.set_led_color(led_id, [0, 255, 255]))

    def test_solid(self):
        color = [255, 0, 255]
        self.assertIsNotNone(self.led_ring.solid(color))
        status = self.led_ring.get_status()
        self.assertEqual(status.mode, LedMode.USER)
        self.assertEqual(status.animation, AnimationMode.SOLID)
        self.assertEqual([status.r, status.g, status.b], [255, 0, 255])

        with self.assertRaises(RobotCommandException):
            self.led_ring.alternate([])

        with self.assertRaises(RobotCommandException):
            self.led_ring.alternate(10)

    def test_custom(self):
        self.assertIsNotNone(self.led_ring.custom(led_colors=[[i / 30. * 255, 0, 255 - i / 30.] for i in range(30)]))
        status = self.led_ring.get_status()
        self.assertEqual(status.mode, LedMode.USER)
        self.assertEqual(status.animation, AnimationMode.CUSTOM)

        with self.assertRaises(RobotCommandException):
            self.led_ring.custom(led_colors=[20 * [3 * [0]]])

        with self.assertRaises(RobotCommandException):
            self.led_ring.custom(led_colors=[30 * [2 * [0]]])


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        print('TEST FUNCTION: ', function_name)
        suite.addTest(TestLedRing(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
