#!/usr/bin/env python
# coding=utf-8

class DigitalPinObject:
    """
    Object used to store information on digital pins
    """

    def __init__(self, name, mode, value):
        # Name
        self.name = name
        # Input or output
        self.mode = mode
        # True / False
        self.value = value

    def __str__(self):
        string_ret = "Name : {}".format(self.name)
        string_ret += ", Mode : {}".format(self.mode)
        string_ret += ", State : {}".format(self.value)
        return string_ret

    def __repr__(self):
        return self.__str__()


class AnalogPinObject:
    """
    Object used to store information on digital pins
    """

    def __init__(self, name, mode, value):
        # Name
        self.name = name
        # Input or output
        self.mode = mode
        # Tension
        self.value = value

    def __str__(self):
        string_ret = "Name : {}".format(self.name)
        string_ret += ", Mode : {}".format(self.mode)
        string_ret += ", State : {}".format(self.value)
        return string_ret

    def __repr__(self):
        return self.__str__()
