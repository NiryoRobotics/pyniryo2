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

robot_ip_address = "192.168.1.13"
port = 9090

test_order = [
            # "test_led_display_robot_status",
              "test_led_controlled_user",
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
        # cls.arm.learning_mode = True
        # cls.arm.go_to_sleep()
        cls.client.terminate()

    def assertHasAttr(self, obj, intendedAttr):
        testBool = hasattr(obj, intendedAttr)
        self.assertTrue(testBool, msg='obj lacking an attribute. obj: %s, intendedAttr: %s' % (obj, intendedAttr))

    # @staticmethod
    # def assertAlmostEqualVector(a, b, decimal=1):
    #     np.testing.assert_almost_equal(a, b, decimal)

# noinspection PyTypeChecker
class TestLedRing(BaseTest):
    neutral_pose = [0.2, 0.0, 0.4, 0., 0., 0.]

    def go_to_neutral_pose(self):
        self.assertIsNone(self.arm.move_pose(self.neutral_pose))

    def test_led_ring_status_obj(self, led_ring_status):
        self.assertHasAttr(led_ring_status, "led_ring_mode")
        self.assertHasAttr(led_ring_status, "animation_mode")
        self.assertHasAttr(led_ring_status, "animation_color")

    def test_led_ring_color_obj(self, led_ring_color_state):
        self.assertIsInstance(led_ring_color_state, list)
        self.assertEqual(len(led_ring_color_state), 30)

    # - Test functions

    def test_led_display_robot_status(self): # TODO : we need to access/publish on robot status to check every status
        # Launch first calibration
        self.assertIsNone(self.arm.calibrate_auto())
        self.go_to_neutral_pose()

        self.assertIsNone(time.sleep(1))

        # - Test Led Ring display learning mode
        print 'TEST LEARNING MODE'
        self.arm.learning_mode = True

        led_ring_status = self.led_ring.get_led_ring_status()
        self.test_led_ring_status_obj(led_ring_status)
        self.assertEqual(led_ring_status.led_ring_mode, LedMode.ROBOT_STATUS.value)
        self.assertEqual(led_ring_status.animation_mode, AnimationMode.SOLID.value)

        led_ring_color_state = self.led_ring.get_led_ring_colors()
        self.test_led_ring_color_obj(led_ring_color_state)
        for i in range(30):
            self.assertEqual(led_ring_color_state[i], WHITE)
        
        self.assertIsNone(time.sleep(1))


        # - Test Led Ring display standby
        print 'TEST STANDBY'
        self.arm.learning_mode = False
        led_ring_status = self.led_ring.get_led_ring_status()
        self.test_led_ring_status_obj(led_ring_status)
        self.assertEqual(led_ring_status.led_ring_mode, LedMode.ROBOT_STATUS.value)
        self.assertEqual(led_ring_status.animation_mode, AnimationMode.SOLID.value)

        led_ring_color_state = self.led_ring.get_led_ring_colors()
        self.test_led_ring_color_obj(led_ring_color_state)
        for i in range(30):
            self.assertEqual(led_ring_color_state[i], GREEN)

        self.assertIsNone(time.sleep(1))

        # - Test Led Ring display moving 
        # Led Ring must be flashing green
        print 'TEST MOVING'
        joints = [0., 0., 0., 0., 0., 0.]
        def check_move_color(color):
            self.test_led_ring_color_obj(color)
            for i in range(30):
                self.assertTrue(color[i] == GREEN or color[i] == NONE)

        def check_move_status(status):
            self.test_led_ring_status_obj(led_ring_status)
            self.assertEqual(led_ring_status.led_ring_mode, LedMode.ROBOT_STATUS.value)
            self.assertEqual(led_ring_status.animation_mode, AnimationMode.FLASHING.value)

        self.led_ring.led_ring_colors.subscribe(check_move_color)
        self.led_ring.led_ring_status.subscribe(check_move_status)
        self.assertIsNone(self.arm.move_joints(joints))
        self.led_ring.led_ring_colors.unsubscribe()
        self.led_ring.led_ring_status.unsubscribe()


    def test_led_controlled_user(self): # TODO : activate autonomous mode first
        
        
        # - NONE
        self.test_user_none()
        self.assertIsNone(self.led_ring.led_ring_turn_off()) 
        self.assertIsNone(time.sleep(1))

        # - SOLID
        self.test_user_solid()
        self.assertIsNone(self.led_ring.led_ring_turn_off()) 
        self.assertIsNone(time.sleep(1))

        # - Flashing
        self.test_user_flash()
        self.assertIsNone(self.led_ring.led_ring_turn_off()) 
        self.assertIsNone(time.sleep(1))

        # - Alternate
        self.test_user_alternate()
        self.assertIsNone(self.led_ring.led_ring_turn_off()) 
        self.assertIsNone(time.sleep(1))

        # - Chase
        self.test_user_chase()
        self.assertIsNone(self.led_ring.led_ring_turn_off()) 
        self.assertIsNone(time.sleep(1))
        
        # - Color wipe
        self.test_user_color_wipe()
        self.assertIsNone(self.led_ring.led_ring_turn_off()) 
        self.assertIsNone(time.sleep(1))
        
        # - Rainbow
        self.test_user_rainbow()
        self.assertIsNone(self.led_ring.led_ring_turn_off()) 
        self.assertIsNone(time.sleep(1))

    def test_user_solid(self):
        print 'TEST USER - SOLID'
        color_solid = [178.0, 189.0, 230.0]
        self.assertIsNone(self.led_ring.led_ring_solid(color_solid)) # TODO : wait ?
        led_ring_status = self.led_ring.get_led_ring_status()
        self.test_led_ring_status_obj(led_ring_status)
        self.assertEqual(led_ring_status.led_ring_mode, LedMode.USER.value)
        self.assertEqual(led_ring_status.animation_mode, AnimationMode.SOLID.value)

        led_ring_color_state = self.led_ring.get_led_ring_colors()
        self.test_led_ring_color_obj(led_ring_color_state)
        for i in range(30):
            self.assertEqual(led_ring_color_state[i], color_solid)


    def test_user_none(self):
        print 'TEST USER - NONE'
        self.assertIsNone(self.led_ring.led_ring_turn_off()) # TODO: test with 'wait'
        led_ring_status = self.led_ring.get_led_ring_status()
        self.test_led_ring_status_obj(led_ring_status)
        self.assertEqual(led_ring_status.led_ring_mode, LedMode.USER.value)
        self.assertEqual(led_ring_status.animation_mode, AnimationMode.NONE.value)

        led_ring_color_state = self.led_ring.get_led_ring_colors()
        self.test_led_ring_color_obj(led_ring_color_state)
        for i in range(30):
            self.assertEqual(led_ring_color_state[i], NONE)


    def test_user_flash(self):
        print 'TEST USER - FLASHING'
        color_flashing = [0.0, 255.0, 164.0]
        iter_flashing = 5 # 1 iter = 1 solid color followed by 1 none (leds turned off)
        freq_flashing = 3.0
        print ' flashing color {} {} times, at freq {} ...'.format(color_flashing, iter_flashing, freq_flashing)
        self.is_flashing = False
        # Variable used to check if flash was correctly done
        self.flash_nb = 0
        self.times_flashing = []
        self.color_flashed = NONE

        def check_color_flash(color):
            if self.is_flashing:
                if not (self.flash_nb == 0 and color[0] == NONE):
                    # If first iteration in the callback, check that the flash really started (color displayed
                    # for the first time)
                    time_now = time.time()
                    self.times_flashing.append(time_now)
                    self.flash_nb = self.flash_nb + 1
                    for i in range(30): # check all leds are the right color
                        self.assertTrue(color[i] == color_flashing or color[i] == NONE) # TODO also check colors
                        if color[i] != NONE:
                            self.color_flashed = color[i]

        def check_status_flash(status):
            if status.animation_mode == AnimationMode.FLASHING.value:
                self.is_flashing = True
            else:
                self.is_flashing = False
            
        self.led_ring.led_ring_status.subscribe(check_status_flash)
        self.led_ring.led_ring_colors.subscribe(check_color_flash)
        self.assertIsNone(self.led_ring.led_ring_flash(color_flashing, wait = True, iterations = iter_flashing, frequency = freq_flashing))
        self.led_ring.led_ring_colors.unsubscribe()
        self.led_ring.led_ring_status.unsubscribe()

        # check the nb of iterations
        self.assertEqual(self.flash_nb, iter_flashing*2) 

        # check the mean frequency
        self.times_between_flashes = [] # 
        for i,k in zip(self.times_flashing[0::2], self.times_flashing[1::2]):
            self.times_between_flashes.append(k-i)
        mean_time_iter = sum(self.times_between_flashes) / len(self.times_between_flashes)
        mean_freq_iter = 1.0/mean_time_iter
        self.assertAlmostEqual(freq_flashing, mean_freq_iter, delta = 0.1 )
        print ' flashed color {} {} times, at mean freq {}'.format(self.color_flashed, self.flash_nb/2, mean_freq_iter)


    def test_user_alternate(self):
        print 'TEST USER - ALTERNATE'
        colors_list = [[22.0,244.0,244.0],[140.0,70.0,220.0],[246.0,31.0,99.0]]
        iter_alternate = 3 # 1 iter = len(colors_list) alternations
        print ' alternate colors {} {} times...'.format(colors_list, iter_alternate)
        self.is_alter = False
        # Variables used to check if alternation was correctly done
        self.alter_nb = 0
        self.colors_alternated_list = []
        def check_color_alternate(color):
            if self.is_alter:
                if not (self.alter_nb == 0 and color[0] == NONE):
                    self.alter_nb = self.alter_nb + 1
                    for i in range(30): # TODO : change 30 with a parameter
                        if color[i] not in self.colors_alternated_list:
                            self.colors_alternated_list.append(color[i])
                        self.assertTrue(color[i] in colors_list)

        def check_status_alternate(status):
            if status.animation_mode == AnimationMode.ALTERNATE.value:
                self.is_alter = True
            else:
                self.is_alter = False

        self.led_ring.led_ring_status.subscribe(check_status_alternate)
        self.led_ring.led_ring_colors.subscribe(check_color_alternate)
        self.assertIsNone(self.led_ring.led_ring_alternate(colors_list, wait = True, iterations = iter_alternate))
        self.led_ring.led_ring_colors.unsubscribe()
        self.led_ring.led_ring_status.unsubscribe()

        # check the nb of iterations
        self.assertEqual(self.alter_nb, iter_alternate*len(colors_list)) 

        # check alternated colors
        self.assertEqual(colors_list, self.colors_alternated_list)
        print ' alternated colors {} {} times'.format(self.colors_alternated_list, self.alter_nb/len(colors_list))

    def test_user_chase(self):
        print 'TEST USER - CHASE'
        color_chase = [255.0, 0.0, 0.0]
        iter_chase = 15 # 1 iter = 3 times leds sets
        speed_chase = 50
        print ' chase color {} {} times at speed {}...'.format(color_chase, iter_chase, speed_chase)
        self.is_chase = False
        # Variables used to check if chase was correctly done
        self.times_chase = []
        self.chase_nb = 0
        self.color_chased = [] # list of colors displayed during the animation

        def check_color_chase(color):
            if self.is_chase:
                if not (self.chase_nb == 0 and color == [NONE]*30):
                    self.times_chase.append(time.time())
                    self.chase_nb = self.chase_nb + 1
                    for i in range(30): # TODO: check that we do the 30
                        if color[i] not in self.color_chased and color[i] != NONE:
                            self.color_chased.append(color[i])                        
                        self.assertTrue(color[i] == color_chase or color[i] == NONE)

        def check_status_chase(status):
            if status.animation_mode == AnimationMode.CHASE.value:
                self.is_chase = True
            else:
                self.is_chase = False

        self.led_ring.led_ring_status.subscribe(check_status_chase)
        self.led_ring.led_ring_colors.subscribe(check_color_chase)
        self.assertIsNone(self.led_ring.led_ring_chase(color_chase, wait = True, iterations = iter_chase, speed = speed_chase))
        self.led_ring.led_ring_colors.unsubscribe()
        self.led_ring.led_ring_status.unsubscribe()

        # check the nb of iterations
        self.assertEqual(self.chase_nb, iter_chase*3) 

        # check color
        self.assertEqual(len(self.color_chased), 1) # TODO : do that also for alternate (and others?)
        self.assertEqual(self.color_chased[0], color_chase)

        # check the mean speed
        self.times_between_chases = [] # 
        for i,k in zip(self.times_chase[0::2], self.times_chase[1::2]):
            self.times_between_chases.append(k-i)
        mean_time_iter = round((sum(self.times_between_chases) / len(self.times_between_chases))*1000.0, 1) # speed chase is in millisecondes
        self.assertAlmostEqual(mean_time_iter, speed_chase, delta = 5)

        print ' chased color {} {} times, at mean speed {}'.format(self.color_chased[0], self.chase_nb/3, mean_time_iter)

    def test_user_color_wipe(self):
        print 'TEST USER - COLOR WIPE'
        color_wipe = [230.0, 79.0, 128.0]
        speed = 60
        print ' color wipe with color {} at speed {}...'.format(color_wipe, speed)
        self.is_wipe = False
        # Variables used to check if chase was correctly done
        self.times_wipe = [] # TODO : rename "speed"
        self.color_wiped = [] # list of colors displayed during the animation
        self.max_index_colored = 0

        def check_color_wipe(color):
            # print color
            if self.is_wipe:
                if not (color == [NONE]*30):
                    self.times_wipe.append(time.time())
                    for i in range(30): 
                        if color[i] not in self.color_wiped and color[i] != NONE:
                            self.color_wiped.append(color[i])         
                        self.assertTrue(color[i] == color_wipe or color[i] == NONE) # IMPORTANT: an assert in a callback won't throw an error...
                        if i > 0 and color[i] == NONE and color[i-1] != NONE:
                            self.max_index_colored = i-1
                        if i == 29 and color[i] != NONE: 
                            self.max_index_colored = i

        def check_status_wipe(status):
            if status.animation_mode == AnimationMode.COLOR_WIPE.value:
                self.is_wipe = True
            else:
                self.is_wipe = False

        self.led_ring.led_ring_status.subscribe(check_status_wipe)
        self.led_ring.led_ring_colors.subscribe(check_color_wipe)
        self.assertIsNone(self.led_ring.led_ring_wipe(color_wipe, wait = True, speed = speed))
        self.led_ring.led_ring_colors.unsubscribe()
        self.led_ring.led_ring_status.unsubscribe()

        # check the wipe was completed
        self.assertEqual(self.max_index_colored+1, 30)

        # check color
        self.assertEquals(len(self.color_wiped), 1)
        self.assertEquals(self.color_wiped[0], color_wipe)

        # check speed
        self.times_between_wipe = [] # 
        for i,k in zip(self.times_wipe[0::2], self.times_wipe[1::2]):
            self.times_between_wipe.append(k-i)
        mean_time_iter = round((sum(self.times_between_wipe) / len(self.times_between_wipe))*1000.0, 1) # speed chase is in millisecondes
        self.assertAlmostEqual(mean_time_iter, speed, delta = 5)
        print ' color wiped with color {} at speed {}...'.format(self.color_wiped[0], mean_time_iter)


    def test_user_rainbow(self):
        print 'TEST USER - RAINBOW'
        iter_rainbow = 2
        # NOTE: if speed too low (rainbow rapid), the values from the color topic subscription won't be correctly retrieved and it errors will be raised
        speed_rainbow = 20
        print ' rainbow {} times at speed {}...'.format(iter_rainbow, speed_rainbow)
        self.is_rainbow = False
        # Variables used to check if rainbow was correctly done
        self.times_rainbow = []

        self.rainbow_values = [float(i) for i in range(0, 256, 3)]
        self.first_led_r_values =[]
        self.first_led_g_values =[]
        self.first_led_b_values =[]
        self.first_led_max_red_reached = 0
        self.first_led_max_green_reached = 0
        self.first_led_max_blue_reached = 0

        def check_color_rainbow(color):
            if self.is_rainbow:
                if not (color == [NONE]*30):
                    self.times_rainbow.append(time.time())
                    self.first_led_r_values.append(color[0][0])
                    self.first_led_g_values.append(color[0][1])
                    self.first_led_b_values.append(color[0][2])
                    if (color[0][0] == 255.0):
                        self.first_led_max_red_reached += 1
                    if (color[0][1] == 255.0): # green is 255.0 at the beginning and the end for the first led
                        self.first_led_max_green_reached += 1
                    if (color[0][2] == 255.0):
                        self.first_led_max_blue_reached += 1


        def check_status_rainbow(status):
            if status.animation_mode == AnimationMode.RAINBOW.value:
                self.is_rainbow = True
            else:
                self.is_rainbow = False

        self.led_ring.led_ring_status.subscribe(check_status_rainbow)
        self.led_ring.led_ring_colors.subscribe(check_color_rainbow)
        self.assertIsNone(self.led_ring.led_ring_rainbow(wait = True, iterations = iter_rainbow, speed = speed_rainbow))
        self.led_ring.led_ring_colors.unsubscribe()
        self.led_ring.led_ring_status.unsubscribe()

        # check that the first led took all rainbow values. 
        # NOTE: we don't check the order of colors here, neither the other leds. todo later
        for rainbow_value in self.rainbow_values:
            self.assertTrue(rainbow_value in self.first_led_r_values)
            self.assertTrue(rainbow_value in self.first_led_g_values)
            self.assertTrue(rainbow_value in self.first_led_b_values)

        # check the nb of iterations. One iteration = each led reaches the max (255.0) of red, green and blue
        self.assertEqual(iter_rainbow, self.first_led_max_red_reached)
        self.assertEqual(iter_rainbow, self.first_led_max_green_reached / 2.0) # green is 255.0 at the beginning and the end for the first led
        self.assertEqual(iter_rainbow, self.first_led_max_blue_reached)

        # check the mean speed
        self.times_between_rainbows = [] # 
        for i,k in zip(self.times_rainbow[0::2], self.times_rainbow[1::2]):
            self.times_between_rainbows.append(k-i)
        mean_time_iter = round((sum(self.times_between_rainbows) / len(self.times_between_rainbows))*1000.0, 1) # speed rainbow is in millisecondes
        self.assertAlmostEqual(mean_time_iter, speed_rainbow, delta = 5)
        print ' rainbow {} times at speed {}...'.format(self.first_led_max_red_reached, mean_time_iter)



def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestLedRing(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
