#!/usr/bin/env python
# coding=utf-8

class DigitalPinObject:
    """
    Object used to store information on digital pins
    """

    def __init__(self, pin_id, name, mode, state):
        # Pin ID
        self.pin_id = pin_id
        # Name
        self.name = name
        # Input or output
        self.mode = mode
        # High or Low
        self.state = state

    def __str__(self):
        string_ret = "Pin : {}".format(self.pin_id)
        string_ret += ", Name : {}".format(self.name)
        string_ret += ", Mode : {}".format(self.mode)
        string_ret += ", State : {}".format(self.state)
        return string_ret

    def __repr__(self):
        return self.__str__()