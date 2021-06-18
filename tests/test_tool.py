#!/usr/bin/env python
import time
import unittest
import roslibpy
import numpy as np
from threading import Event

from exceptions import RobotCommandException
from niryo_topic import NiryoTopic
from enums import RobotErrors
from io.enums import PinID
from tool.tool import Tool
from tool.enums import ToolID

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
        self.assertTrue(self.tool.update_tool())
        self.assertIsNone(time.sleep(1))

        tool_update_event = Event()
        tool_update_event.clear()

        def tool_update_callback(result):
            self.assertTrue(result["status"] >= RobotErrors.SUCCESS.value)
            tool_update_event.set()

        self.assertTrue(self.tool.update_tool(tool_update_callback))
        self.assertTrue(tool_update_event.wait(10))

    def test_electromagnet(self):
        # Setup
        with self.assertRaises(RobotCommandException):
            self.tool.setup_electromagnet(0)

        self.assertTrue(self.tool.setup_electromagnet(PinID.GPIO_1A))
        self.assertEqual(self.tool.get_current_tool_id(), ToolID.ELECTROMAGNET_1)
        # Activate
        self.assertTrue(self.tool.activate_electromagnet())
        self.assertTrue(self.tool.activate_electromagnet(PinID.GPIO_1A))

        tool_event = Event()
        tool_event.clear()

        def tool_callback(_):
            tool_event.set()

        self.assertTrue(self.tool.activate_electromagnet(callback=tool_callback))
        self.assertTrue(tool_event.wait(10))

        # Deactivate
        self.assertTrue(self.tool.deactivate_electromagnet())
        self.assertTrue(self.tool.deactivate_electromagnet(PinID.GPIO_1A))

        tool_event.clear()

        self.assertTrue(self.tool.deactivate_electromagnet(callback=tool_callback))
        self.assertTrue(tool_event.wait(10))

        self.assertTrue(self.tool.grasp_with_tool())
        self.assertTrue(self.tool.release_with_tool())

        # Exceptions
        with self.assertRaises(RobotCommandException):
            self.tool.activate_electromagnet(pin_id=5)
        with self.assertRaises(RobotCommandException):
            self.tool.deactivate_electromagnet(pin_id=5)
        self.assertTrue(self.tool.update_tool())
        with self.assertRaises(RobotCommandException):
            self.tool.activate_electromagnet()
        with self.assertRaises(RobotCommandException):
            self.tool.deactivate_electromagnet()

    def test_grippers(self):
        self.assertTrue(self.tool.update_tool())

        tool_event = Event()

        def tool_callback(_):
            tool_event.set()

        if self.tool.get_current_tool_id() in [ToolID.GRIPPER_1, ToolID.GRIPPER_2, ToolID.GRIPPER_3]:
            self.assertTrue(self.tool.open_gripper())
            self.assertTrue(self.tool.open_gripper(800))
            self.assertTrue(self.tool.open_gripper(speed=800.5))
            tool_event.clear()
            self.assertTrue(self.tool.open_gripper(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            with self.assertRaises(RobotCommandException):
                self.tool.open_gripper(-10)
            with self.assertRaises(RobotCommandException):
                self.tool.open_gripper(0)
            with self.assertRaises(RobotCommandException):
                self.tool.open_gripper(1001)

            self.assertTrue(self.tool.close_gripper())
            self.assertTrue(self.tool.close_gripper(800))
            self.assertTrue(self.tool.close_gripper(speed=800.5))
            tool_event.clear()
            self.assertTrue(self.tool.close_gripper(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            with self.assertRaises(RobotCommandException):
                self.tool.close_gripper(-10)
            with self.assertRaises(RobotCommandException):
                self.tool.close_gripper(0)
            with self.assertRaises(RobotCommandException):
                self.tool.close_gripper(1001)

            self.assertTrue(self.tool.grasp_with_tool())
            self.assertTrue(self.tool.release_with_tool())

            tool_event.clear()
            self.assertTrue(self.tool.grasp_with_tool(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            tool_event.clear()
            self.assertTrue(self.tool.release_with_tool(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

        # Exceptions
        self.assertTrue(self.tool.setup_electromagnet(PinID.GPIO_1A))
        with self.assertRaises(RobotCommandException):
            self.tool.open_gripper()
        with self.assertRaises(RobotCommandException):
            self.tool.close_gripper()

    def test_vacuum_pump(self):
        self.assertTrue(self.tool.update_tool())

        tool_event = Event()

        def tool_callback(_):
            tool_event.set()

        if self.tool.get_current_tool_id() in [ToolID.VACUUM_PUMP_1, ]:
            self.assertTrue(self.tool.pull_air_vacuum_pump())
            tool_event.clear()
            self.assertTrue(self.tool.pull_air_vacuum_pump(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            self.assertTrue(self.tool.push_air_vacuum_pump())
            tool_event.clear()
            self.assertTrue(self.tool.push_air_vacuum_pump(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            self.assertTrue(self.tool.grasp_with_tool())
            self.assertTrue(self.tool.release_with_tool())

            tool_event.clear()
            self.assertTrue(self.tool.grasp_with_tool(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

            tool_event.clear()
            self.assertTrue(self.tool.release_with_tool(callback=tool_callback))
            self.assertTrue(tool_event.wait(10))

        # Exceptions
        self.assertTrue(self.tool.setup_electromagnet(PinID.GPIO_1A))
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
