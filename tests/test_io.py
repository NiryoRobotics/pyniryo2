#!/usr/bin/env python
import unittest
import roslibpy
from threading import Event

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_topic import NiryoTopic

from pyniryo2.io.enums import PinID, PinMode, PinState
from pyniryo2.io.objects import DigitalPinObject
from pyniryo2.io.io import IO


robot_ip_address = "192.168.1.52"
port = 9090

test_order = ["get_io_sate",
              "test_pin_mode",
              "test_set_pin_state",
              ]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = roslibpy.Ros(host=robot_ip_address, port=port)
        cls.client.run()
        cls.io = IO(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.terminate()


# noinspection PyTypeChecker
class TestIO(BaseTest):
    def get_io_sate(self):
        self.assertIsInstance(self.io.get_digital_io_states, NiryoTopic)
        self.assertIsInstance(self.io.get_digital_io_states(), list)
        io_state = self.io.get_digital_io_states()
        self.assertIsInstance(self.io.get_digital_io_state(PinID.GPIO_1A), DigitalPinObject)
        io_state_bis = self.io.get_digital_io_state(PinID.GPIO_1A)
        self.assertIsInstance(self.io.digital_read(PinID.GPIO_1A), PinState)

        self.assertIsInstance(io_state, list)
        self.assertIsInstance(io_state[0], DigitalPinObject)
        self.assertIsInstance(io_state[0].pin_id, PinID)
        self.assertEqual(io_state[0].pin_id, io_state_bis.pin_id)
        self.assertIsInstance(io_state[0].name, str)
        self.assertEqual(io_state[0].name, io_state_bis.name)
        self.assertIsInstance(io_state[0].mode, PinMode)
        self.assertEqual(io_state[0].mode, io_state_bis.mode)
        self.assertIsInstance(io_state[0].state, PinState)
        self.assertEqual(io_state[0].state, self.io.digital_read(PinID.GPIO_1A))
        self.assertEqual(io_state[0].state, io_state_bis.state)

        io_state_event = Event()
        io_state_event.clear()

        def io_state_callback(io_state_list):
            self.assertIsInstance(io_state_list, list)
            self.assertIsInstance(io_state_list[0], DigitalPinObject)
            io_state_event.set()

        self.assertIsNone(self.io.get_digital_io_states.subscribe(io_state_callback))
        self.assertTrue(io_state_event.wait(10))
        self.assertIsNone(self.io.get_digital_io_states.unsubscribe())

    def test_pin_mode(self):
        self.assertIsNone(self.io.set_pin_mode(PinID.GPIO_1A, PinMode.INPUT))
        self.assertEqual(self.io.get_digital_io_state(PinID.GPIO_1A).mode,  PinMode.INPUT)
        self.assertIsNone(self.io.set_pin_mode(PinID.GPIO_1A, PinMode.OUTPUT))
        self.assertEqual(self.io.get_digital_io_state(PinID.GPIO_1A).mode, PinMode.OUTPUT)

        with self.assertRaises(RobotCommandException):
            self.io.set_pin_mode(1, PinMode.OUTPUT)

        with self.assertRaises(RobotCommandException):
            self.io.set_pin_mode(PinID.GPIO_1A, 0)

    def test_set_pin_state(self):
        self.assertIsNone(self.io.set_pin_mode(PinID.GPIO_1A, PinMode.INPUT))
        self.assertEqual(self.io.get_digital_io_state(PinID.GPIO_1A).mode,  PinMode.INPUT)

        with self.assertRaises(RobotCommandException):
            self.io.digital_write(PinID.GPIO_1A, PinState.HIGH)

        self.assertIsNone(self.io.set_pin_mode(PinID.GPIO_1A, PinMode.OUTPUT))
        self.assertEqual(self.io.get_digital_io_state(PinID.GPIO_1A).mode, PinMode.OUTPUT)

        self.assertIsNone(self.io.digital_write(PinID.GPIO_1A, PinState.HIGH))
        self.assertEqual(self.io.get_digital_io_state(PinID.GPIO_1A).state, PinState.HIGH)
        self.assertEqual(self.io.digital_read(PinID.GPIO_1A), PinState.HIGH)
        self.assertIsNone(self.io.digital_write(PinID.GPIO_1A, PinState.LOW))
        self.assertEqual(self.io.get_digital_io_state(PinID.GPIO_1A).state, PinState.LOW)
        self.assertEqual(self.io.digital_read(PinID.GPIO_1A), PinState.LOW)

        with self.assertRaises(RobotCommandException):
            self.io.digital_write(1, PinState.LOW)

        with self.assertRaises(RobotCommandException):
            self.io.digital_write(PinID.GPIO_1A, 0)


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestIO(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
