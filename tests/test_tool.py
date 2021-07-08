#!/usr/bin/env python
import time
import unittest
import roslibpy
import numpy as np
from threading import Event

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_topic import NiryoTopic
from pyniryo2.enums import RobotErrors

from pyniryo2.tool.tool import Tool
from pyniryo2.tool.enums import ToolID

from pyniryo2.io.io import IO
from pyniryo2.io.enums import PinID, PinState, PinMode

robot_ip_address = "192.168.1.52"
port = 9090

test_order = ["test_tool_id",
              "test_update_tool",
              "test_electromagnet",
              "test_grippers",
              "test_vacuum_pump",
              ]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = roslibpy.Ros(host=robot_ip_address, port=port)
        cls.client.run()
        cls.tool = Tool(cls.client)
        cls.io = IO(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.terminate()

    @staticmethod
    def assertAlmostEqualVector(a, b, decimal=1):
        np.testing.assert_almost_equal(a, b, decimal)


# noinspection PyTypeChecker
class TestTool(BaseTest):

    def test_tool_id(self):
        self.assertIsNone(time.sleep(1))
        self.assertIsInstance(self.tool.tool, ToolID)
        self.assertIsInstance(self.tool.get_current_tool_id, NiryoTopic)
        self.assertIsInstance(self.tool.get_current_tool_id(), ToolID)

        tool_id_event = Event()
        tool_id_event.clear()

        def tool_id_callback(tool_id):
            tool_id_event.set()
            self.assertIsInstance(tool_id, ToolID)

        self.assertIsNone(self.tool.get_current_tool_id.subscribe(tool_id_callback))
        self.assertTrue(tool_id_event.wait(10))
        self.assertIsNone(self.tool.get_current_tool_id.unsubscribe())

    def test_update_tool(self):
        self.assertIsNone(time.sleep(1))
        self.assertIsNone(self.tool.update_tool())
        self.assertIsNone(time.sleep(1))

        tool_update_event = Event()
        tool_update_event.clear()

        def tool_update_callback(result):
            self.assertTrue(result["status"] >= RobotErrors.SUCCESS.value)
            tool_update_event.set()

        self.assertIsNone(self.tool.update_tool(tool_update_callback))
        self.assertTrue(tool_update_event.wait(10))

    def test_electromagnet(self):
        # Setup
        with self.assertRaises(RobotCommandException):
            self.tool.setup_electromagnet(0)

        self.assertIsNone(self.io.set_pin_mode(PinID.GPIO_1A, PinMode.INPUT))
        self.assertIsNone(self.tool.setup_electromagnet(PinID.GPIO_1A))
        self.assertEqual(self.tool.get_current_tool_id(), ToolID.ELECTROMAGNET_1)
        self.assertEqual(self.io.get_digital_io_state(PinID.GPIO_1A).mode, PinMode.OUTPUT)

        self.assertIsNone(self.tool.activate_electromagnet())
        self.assertEqual(self.io.digital_read(PinID.GPIO_1A), PinState.HIGH)
        self.assertIsNone(self.tool.deactivate_electromagnet())
        self.assertEqual(self.io.digital_read(PinID.GPIO_1A), PinState.LOW)

        self.assertIsNone(self.tool.activate_electromagnet(PinID.GPIO_1A))
        self.assertEqual(self.io.digital_read(PinID.GPIO_1A), PinState.HIGH)
        self.assertIsNone(self.tool.deactivate_electromagnet(PinID.GPIO_1A))
        self.assertEqual(self.io.digital_read(PinID.GPIO_1A), PinState.LOW)

        tool_event = Event()
        tool_event.clear()

        def tool_callback(_):
            tool_event.set()

        self.assertIsNone(self.tool.activate_electromagnet(callback=tool_callback))
        self.assertTrue(tool_event.wait(10))
        self.assertEqual(self.io.digital_read(PinID.GPIO_1A), PinState.HIGH)
        tool_event.clear()

        self.assertIsNone(self.tool.deactivate_electromagnet(callback=tool_callback))
        self.assertTrue(tool_event.wait(10))
        self.assertEqual(self.io.digital_read(PinID.GPIO_1A), PinState.LOW)

        self.assertIsNone(self.tool.grasp_with_tool())
        self.assertEqual(self.io.digital_read(PinID.GPIO_1A), PinState.HIGH)
        self.assertIsNone(self.tool.release_with_tool())
        self.assertEqual(self.io.digital_read(PinID.GPIO_1A), PinState.LOW)

        # Exceptions
        with self.assertRaises(RobotCommandException):
            self.tool.activate_electromagnet(pin_id=5)
        with self.assertRaises(RobotCommandException):
            self.tool.deactivate_electromagnet(pin_id=5)
        self.assertIsNone(self.tool.update_tool())
        with self.assertRaises(RobotCommandException):
            self.tool.activate_electromagnet()
        with self.assertRaises(RobotCommandException):
            self.tool.deactivate_electromagnet()

    def test_grippers(self):
        self.assertIsNone(self.tool.update_tool())

        tool_event = Event()

        def tool_callback(_):
            tool_event.set()

        if self.tool.get_current_tool_id() in [ToolID.GRIPPER_1, ToolID.GRIPPER_2, ToolID.GRIPPER_3]:
            self.assertIsNone(self.tool.open_gripper())
            self.assertIsNone(self.tool.open_gripper(800))
            self.assertIsNone(self.tool.open_gripper(speed=800.5))
            tool_event.clear()
            self.assertIsNone(self.tool.open_gripper(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            with self.assertRaises(RobotCommandException):
                self.tool.open_gripper(-10)
            with self.assertRaises(RobotCommandException):
                self.tool.open_gripper(0)
            with self.assertRaises(RobotCommandException):
                self.tool.open_gripper(1001)

            self.assertIsNone(self.tool.close_gripper())
            self.assertIsNone(self.tool.close_gripper(800))
            self.assertIsNone(self.tool.close_gripper(speed=800.5))
            tool_event.clear()
            self.assertIsNone(self.tool.close_gripper(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            with self.assertRaises(RobotCommandException):
                self.tool.close_gripper(-10)
            with self.assertRaises(RobotCommandException):
                self.tool.close_gripper(0)
            with self.assertRaises(RobotCommandException):
                self.tool.close_gripper(1001)

            self.assertIsNone(self.tool.grasp_with_tool())
            self.assertIsNone(self.tool.release_with_tool())

            tool_event.clear()
            self.assertIsNone(self.tool.grasp_with_tool(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            tool_event.clear()
            self.assertIsNone(self.tool.release_with_tool(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

        # Exceptions
        self.assertIsNone(self.tool.setup_electromagnet(PinID.GPIO_1A))
        with self.assertRaises(RobotCommandException):
            self.tool.open_gripper()
        with self.assertRaises(RobotCommandException):
            self.tool.close_gripper()

    def test_vacuum_pump(self):
        self.assertIsNone(self.tool.update_tool())

        tool_event = Event()

        def tool_callback(_):
            tool_event.set()

        if self.tool.get_current_tool_id() in [ToolID.VACUUM_PUMP_1, ]:
            self.assertIsNone(self.tool.pull_air_vacuum_pump())
            tool_event.clear()
            self.assertIsNone(self.tool.pull_air_vacuum_pump(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            self.assertIsNone(self.tool.push_air_vacuum_pump())
            tool_event.clear()
            self.assertIsNone(self.tool.push_air_vacuum_pump(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            self.assertIsNone(self.tool.grasp_with_tool())
            self.assertIsNone(self.tool.release_with_tool())

            tool_event.clear()
            self.assertIsNone(self.tool.grasp_with_tool(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            tool_event.clear()
            self.assertIsNone(self.tool.release_with_tool(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

        # Exceptions
        self.assertIsNone(self.tool.setup_electromagnet(PinID.GPIO_1A))
        with self.assertRaises(RobotCommandException):
            self.tool.pull_air_vacuum_pump()
        with self.assertRaises(RobotCommandException):
            self.tool.push_air_vacuum_pump()


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestTool(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
