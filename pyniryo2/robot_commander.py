# - Imports
from __future__ import print_function

# Python libraries
# /

# Communication imports
from .exceptions import RobotCommandException


class RobotCommander(object):
    def __init__(self, client):
        self._client = client

        self._services = None
        self._topics = None
        self._actions = None

    def __str__(self):
        return "NiryoRobot"

    def __repr__(self):
        return self.__str__()


    # Parameters checker
    def _check_enum_belonging(self, value, enum_):
        """
        Check if a value belong to an enum
        """
        if value not in enum_:
            self._raise_exception_expected_choice([v for v in enum_], value)

    def _check_list_belonging(self, value, list_):
        """
        Check if a value belong to a list
        """
        if value not in list_:
            self._raise_exception_expected_choice(list_, value)

    def _check_range_belonging(self, value, range_min, range_max):
        """
        Check if a value belong to a range
        """
        if not range_min <= value <= range_max:
            self._raise_exception_expected_range(range_min, range_max, value)

    def _check_dict_belonging(self, value, dict_):
        """
        Check if a value belong to a dictionary
        """
        if value not in dict_.keys():
            self._raise_exception_expected_choice(dict_.keys(), value)

    def _check_type(self, value, type_):
        if type(value) is not type_:
            self._raise_exception_expected_type(type_.__name__, value)

    def _check_instance(self, value, type_):
        if not isinstance(value, type_):
            self._raise_exception_expected_type(type_.__name__, value)

    def _check_list_type(self, values_list, type_):
        for value in values_list:
            self._check_type(value, type_)

    def _map_list(self, list_, type_):
        """
        Try to map a list to another type (Very useful for list like joints
        which are acquired as string)
        """
        try:
            map_list = list(map(type_, list_))
            return map_list
        except ValueError:
            self._raise_exception_expected_type(type_.__name__, list_)

    def _transform_to_type(self, value, type_):
        """
        Try to change value type to another
        """
        try:
            value = type_(value)
            return value
        except ValueError:
            self._raise_exception_expected_type(type_.__name__, value)

    # Error Handlers
    def _raise_exception_expected_choice(self, expected_choice, given):
        raise RobotCommandException("Expected one of the following: {}.\nGiven: {}".format(expected_choice, given))

    def _raise_exception_expected_type(self, expected_type, given):
        raise RobotCommandException("Expected type: {}.\nGiven: {}".format(expected_type, given))

    def _raise_exception_expected_range(self, range_min, range_max, given):
        raise RobotCommandException(
            "Expected the following condition: {} <= value <= {}\nGiven: {}".format(range_min, range_max, given))

    def _raise_exception(self, message):
        raise RobotCommandException("Exception message : {}".format(message))
