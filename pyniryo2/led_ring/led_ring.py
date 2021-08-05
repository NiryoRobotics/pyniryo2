# - Imports
import numpy as np

from pyniryo2.robot_commander import RobotCommander
# from pyniryo2.objects import PoseObject

from .services import LedRingServices
from .topics import LedRingTopics
from .enums import AnimationMode


class LedRing(RobotCommander):
    # --- Public functions --- #
    def __init__(self, client):
        super(LedRing, self).__init__(client)

        self._services = LedRingServices(self._client)
        self._topics = LedRingTopics(self._client)
        # self.__action_timeout = 10

    # - Get current status and state of led ring

    @property
    def led_ring_status(self): 
        """
        Returns the Led Ring status client which can be used synchronously or asynchronously
        to obtain the current Led Ring status.
        :return: Led Ring status topic.
        :rtype: NiryoTopic
        """
        return self._topics.led_ring_status_topic

    def get_led_ring_status(self):
        """
        Get Led Ring status.

        :return: Object with the current led ring mode, the animation played and the color used
        :rtype: LedRingStatusObject
        """
        return self._topics.led_ring_status_topic()

    @property
    def led_ring_colors(self):
        """
        Returns the Led Ring state client which can be used synchronously or asynchronously
        to obtain the current state (color) of each Led of the Led Ring.
        :return: Led Ring state topic.
        :rtype: NiryoTopic
        """
        return self._topics.led_ring_state_topic

    def get_led_ring_colors(self):
        """
        Get a list of color values of each Led.

        :return: list[list[float]] containing color information (r, g and b)
        :rtype: LedRingStateObject
        """
        return self._topics.led_ring_state_topic()


    # - Control Led Ring with available animations

    def led_ring_solid(self, color, wait = False):
        """
        Set the whole Led Ring to a fixed color. 

        Once the robot is in Autonomous mode, 
        You can set the Led Ring color's to red with: ::

            led_ring = robot.led_ring
            led_ring.led_ring_solid([255.0, 0, 0])

        :param color: Led ring color, in a list of size 3 (r, g, b: 0-255) 
        :type color: list[float] or list[int]
        :param wait: The service wait for the animation to finish or not to answer. 
                For this method, the action is quickly done, so waiting doesn't take a lot of time.
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        color = self._check_color_led_ring(color)
        req = self._services.set_led_ring_request(AnimationMode.SOLID.value, color = color, wait = wait)
        self._services.set_led_ring_service.call(req)  # TODO : should we return something ? Like "interrupted" / "launched"?

    def led_ring_turn_off(self, wait = False):
        """
        Turn off all Leds

        You can turn off leds with ::

            led_ring = robot.led_ring
            led_ring.led_ring_turn_off()

        :param wait: the service wait for the animation to finish or not to answer. 
                For this method, the action is quickly done, so waiting doesn't take a lot of time.
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        req = self._services.set_led_ring_request(AnimationMode.NONE.value, wait = wait)
        self._services.set_led_ring_service.call(req)

    def led_ring_flash(self, color, frequency = 4, iterations = 0, wait=False):
        """
        Flashes a color according to a frequency.

        You can make the Led Ring flash a green color 10 times at
        3 Hz with ::

            led_ring = robot.led_ring
            led_ring.led_ring_flash([0, 255, 0], frequency = 3, iterations = 10, wait = True)

        :param color: Led ring color, in a list of size 3 (r, g, b: 0-255) 
        :type color: list[float] or list[int]
        :param frequency: flashing frequency, in Hertz. From 1 Hz to 100 Hz. If 0 or not filled, the default 
                frequency is used (4 Hz)
        :type frequency: int
        :param iterations: Number of consecutives flashes. If 0, the Led Ring flashes endlessly.
        :type iterations: int
        :param wait: The service wait for the animation to finish all iterations or not to answer. If iterations
                is 0, the service answers immediatly. 
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        color = self._check_color_led_ring(color)
        self._check_type(frequency, int)
        self._check_type(iterations, int)
        req = self._services.set_led_ring_request(AnimationMode.FLASHING.value, color = color, frequency = frequency, iterations = iterations, wait = wait)
        self._services.set_led_ring_service.call(req)

    def led_ring_alternate(self, color_list, iterations = 0, wait=False):
        """
        Several colors are alternated one after the other.

        You can make alternate 3 colors endlessly with: ::

            led_ring = robot.led_ring
            color_list = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

            led_ring.led_ring_alternate(color_list)
            # led_ring.led_ring_alternate(color_list, wait = True) # same effect. Won't wait because iterations = 0

        :param color: Led ring color, in a list of size 3 (r, g, b: 0-255) 
        :type color: list[float] or list[int]
        :param iterations: Number of consecutives alternations. If 0, the Led Ring alternates endlessly.
        :type iterations: int
        :param wait: The service wait for the animation to finish all iterations or not to answer. If iterations
                is 0, the service answers immediatly. 
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        for index, color in enumerate(color_list):
            color = self._check_color_led_ring(color)
            color_list[index] = color
        self._check_type(iterations, int)
        req = self._services.set_led_ring_request(AnimationMode.ALTERNATE.value, color_list = color_list, iterations = iterations, wait = wait)
        self._services.set_led_ring_service.call(req)

    def led_ring_chase(self, color, speed = 50, iterations = 0, wait=False):
        """
        Movie theater light style chaser animation.

        You can start a white chase animation with: ::

            led_ring = robot.led_ring
            led_ring.led_ring_chase([255, 255, 255], speed = 60)

        :param color: Led ring color, in a list of size 3 (r, g, b: 0-255) 
        :type color: list[float] or list[int]
        :param speed: Speed of animation between each step, in milliseconde. 
            the bigger this param is, the slower the animation will be. If 0 or
            not filled, the default speed is used (50 ms)
        :type speed: int
        :param iterations: Number of consecutives chase. If 0, the animation continues endlessly.
            One chase just lights one Led every 3 Leds.
        :type iterations: int
        :param wait: The service wait for the animation to finish all iterations or not to answer. If iterations
                is 0, the service answers immediatly. 
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        color = self._check_color_led_ring(color)
        self._check_type(speed, int)
        self._check_type(iterations, int)
        req = self._services.set_led_ring_request(AnimationMode.CHASE.value, color = color, speed = speed, iterations = iterations, wait = wait)
        self._services.set_led_ring_service.call(req)

    def led_ring_wipe(self, color, speed = 50, wait=False):
        """ 
        Wipe a color across the Led Ring, light a Led at a time.

        You can launch a color wipe and wait for the end with: ::

            led_ring = robot.led_ring
            led_ring.led_ring_wipe([255, 255, 0], speed = 100, wait = True)

        :param color: Led ring color, in a list of size 3 (r, g, b: 0-255) 
        :type color: list[float] or list[int]
        :param speed: Speed of animation between each step, in milliseconde. 
            the bigger this param is, the slower the animation will be. If 0 or
            not filled, the default speed is used (50 ms)
        :type speed: int
        :param wait: The service wait for the animation to finish or not to answer.
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        color = self._check_color_led_ring(color)
        self._check_type(speed, int)
        req = self._services.set_led_ring_request(AnimationMode.COLOR_WIPE.value, color = color, speed = speed, wait = wait)
        self._services.set_led_ring_service.call(req)

    def led_ring_rainbow(self, speed = 20, iterations = 0, wait=False):
        """
        Draw rainbow that fades across all Leds at once.

        You can launch a rainbow and wait for the end with: ::

            led_ring = robot.led_ring
            led_ring.led_ring_rainbow(speed = 10, iterations = 1, wait = True)

        :param speed: Speed of animation between each step, in milliseconde. 
            the bigger this param is, the slower the animation will be. If 0 or
            not filled, the default speed is used (20 ms)
        :type speed: int
        :param iterations: Number of consecutives rainbows. If 0, the animation continues endlessly.
        :type iterations: int
        :param wait: The service wait for the animation to finish or not to answer. If iterations
                is 0, the service answers immediatly. 
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        self._check_type(speed, int)
        self._check_type(iterations, int)
        req = self._services.set_led_ring_request(AnimationMode.RAINBOW.value, speed = speed, iterations = iterations, wait = wait)
        self._services.set_led_ring_service.call(req)

    def led_ring_rainbow_cycle(self, speed = 20, iterations = 0, wait=False):
        """
        Draw rainbow that uniformly distributes itself across all Leds.

        You can launch an endless rainbow cycle  ::

            led_ring = robot.led_ring
            led_ring.led_ring_rainbow_cycle(speed = 10)

        :param speed: Speed of animation between each step, in milliseconde. 
            the bigger this param is, the slower the animation will be. If 0 or
            not filled, the default speed is used (20 ms)
        :type speed: int
        :param iterations: Number of consecutives rainbow cycles. If 0, the animation continues endlessly.
        :type iterations: int
        :param wait: The service wait for the animation to finish or not to answer. If iterations
                is 0, the service answers immediatly. 
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        self._check_type(speed, int)
        self._check_type(iterations, int)
        req = self._services.set_led_ring_request(AnimationMode.RAINBOW_CYLE.value, speed = speed, iterations = iterations, wait = wait)
        self._services.set_led_ring_service.call(req)

    def led_ring_rainbow_chase(self, speed = 50, iterations = 0, wait=False):
        """
        Rainbow chase animation, like the led_ring_chase method.

        You can launch an endless rainbow cycle  ::

            led_ring = robot.led_ring
            led_ring.led_ring_rainbow_chase(speed = 10)

        :param speed: Speed of animation between each step, in milliseconde. 
            the bigger this param is, the slower the animation will be. If 0 or
            not filled, the default speed is used (50 ms)
        :type speed: int
        :param iterations: Number of consecutives rainbow cycles. If 0, the animation continues endlessly.
        :type iterations: int
        :param wait: The service wait for the animation to finish or not to answer. If iterations
                is 0, the service answers immediatly. 
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        self._check_type(speed, int)
        self._check_type(iterations, int)
        req = self._services.set_led_ring_request(AnimationMode.RAINBOW_CHASE.value, speed = speed, iterations = iterations, wait = wait)
        self._services.set_led_ring_service.call(req)

    def led_ring_go_up(self, color, speed = 50, iterations = 0, wait=False):
        """
        Leds turn on like a loading circle, and are then all turned off at once.

        You can launch 2 go up animations and wait for the end ::

            led_ring = robot.led_ring
            led_ring.led_ring_go_up([0, 255, 255], iterations = 2, wait = True)

        :param color: Led ring color, in a list of size 3 (r, g, b: 0-255) 
        :type color: list[float] or list[int]
        :param speed: Speed of animation between each step, in milliseconde. 
            the bigger this param is, the slower the animation will be. If 0 or
            not filled, the default speed is used (50 ms)
        :type speed: int
        :param iterations: Number of consecutives turns around the Led Ring. If 0, the animation 
            continues endlessly.
        :type iterations: int
        :param wait: The service wait for the animation to finish or not to answer. If iterations
                is 0, the service answers immediatly. 
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        color = self._check_color_led_ring(color)
        self._check_type(speed, int)
        self._check_type(iterations, int)
        req = self._services.set_led_ring_request(AnimationMode.GO_UP.value, color = color, speed = speed, iterations = iterations, wait = wait)
        self._services.set_led_ring_service.call(req)

    def led_ring_go_up_down(self, color, speed = 0, iterations = 0, wait=False):
        """
        Leds turn on like a loading circle, and are turned off the same way.

        You can launch 1 go up and down animations and wait for the end ::

            led_ring = robot.led_ring
            led_ring.led_ring_go_up([255, 255, 255], iterations = 1, wait = True)

        :param color: Led ring color, in a list of size 3 (r, g, b: 0-255) 
        :type color: list[float] or list[int]
        :param speed: Speed of animation between each step, in milliseconde. 
            the bigger this param is, the slower the animation will be. If 0 or
            not filled, the default speed is used (50 ms)
        :type speed: int
        :param iterations: Number of consecutives turns around the Led Ring. If 0, the animation 
            continues endlessly.
        :type iterations: int
        :param wait: The service wait for the animation to finish or not to answer. If iterations
                is 0, the service answers immediatly. 
        :type wait: bool
        :rtype: None
        """
        self._check_type(wait, bool)
        color = self._check_color_led_ring(color)
        self._check_type(speed, int)
        self._check_type(iterations, int)
        req = self._services.set_led_ring_request(AnimationMode.GO_UP_AND_DOWN.value, color = color, speed = speed, iterations = iterations, wait = wait)
        self._services.set_led_ring_service.call(req)


    # Usefull method Led Ring
    def _check_color_led_ring(self, color):
        self._check_type(color, list)
        if len(color) != 3: 
            self._raise_exception("Color must be a list of size 3: [r, g, b]")
        for index, color_elem in enumerate(color):
            if color_elem < 0 or color_elem > 255:
                self._raise_exception_expected_range(0, 255, color_elem)
            color[index] = self._transform_to_type(color_elem, float)
        return color