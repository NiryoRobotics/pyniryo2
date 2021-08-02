#!/usr/bin/env python
# coding=utf-8

from pyniryo2.led_ring.enums import AnimationMode, LedMode

class LedRingStatusObject:
    """
    Object used to store Led Ring status
    """

    def __init__(self):
        # Number representing the current Led mode : 1 when displaying robot status, 2 when controlled by user
        self.led_ring_mode = None
        # Number representing the current animation (from -1 for NONE to 10 for GO UP AND DOWN), see LedRingAnimation message
        self.animation_mode = -1
        # 3 sized list indicating current displayed color, except for the Rainbow animation
        self.animation_color = None


    def init_from_message(self, msg):
        self.led_ring_mode = msg["led_mode"]
        self.animation_mode = msg["animation_mode"]["animation"]
        self.animation_color = [msg["animation_color"]["r"], msg["animation_color"]["g"], msg["animation_color"]["b"]] 


    def init_from_values(self, led_ring_mode, animation_mode, animation_color):
        self.led_ring_mode = led_ring_mode
        self.animation_mode = animation_mode
        self.animation_color = animation_color

    def __str__(self):
        list_string_ret = list()
        list_string_ret.append("Current mode : {}".format(LedMode(self.led_ring_mode).name))
        list_string_ret.append("Animation played : {}".format(AnimationMode(self.animation_mode).name))
        list_string_ret.append("Animation color : {}".format(self.animation_color))
        return "\n".join(list_string_ret)

    def __repr__(self):
        return self.__str__()


class LedRingStateObject:
    """
    Object used to store Led Ring state (current color of each Led)
    """

    def __init__(self):
        # 30 sized list of colors [r, g, b]
        self.led_state = None

    def init_from_message(self, msg):
        led_state = []
        for color_rgba_obj in msg["led_ring_colors"]:
            color_rgb = []
            color_rgb.append(color_rgba_obj["r"]) # or color_rgba_obj["r"]
            color_rgb.append(color_rgba_obj["g"]) # or color_rgba_obj["r"]
            color_rgb.append(color_rgba_obj["b"]) # or color_rgba_obj["r"]
            led_state.append(color_rgb)
        self.led_state = led_state

    def __str__(self):
        list_string_ret = list()
        list_string_ret.append("Color list: {}".format(self.led_state))
        return "\n".join(list_string_ret)

    def __repr__(self):
        return self.__str__()
