#!/usr/bin/env python
import time

import sys
import unittest
import roslibpy
import numpy as np
from threading import Event

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.arm.arm import Arm
from pyniryo2.arm.enums import CalibrateMode


robot_ip_address = "192.168.1.52"
port = 9090


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = roslibpy.Ros(host=robot_ip_address, port=port)
        cls.client.run()
        cls.arm = Arm(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.terminate()

    @staticmethod
    def assertAlmostEqualVector(a, b, decimal=1):
        np.testing.assert_almost_equal(a, b, decimal)

# noinspection PyTypeChecker
class TestHardwareStatus(BaseTest):

    def test_topic(self):
        self.assertIsNotNone(self.arm.hardware_status())
        self.assertIsNotNone(self.arm.hardware_status.value)


    # def test_synchronous_calibration(self):
    #     # Test Reset calibration
    #     self.assertIsNone(self.arm.reset_calibration())
    #     self.assertTrue(self.arm.need_calibration())
    #
    #     # Test Auto calibration
    #     self.assertTrue(self.arm.calibrate(CalibrateMode.AUTO))
    #     self.assertFalse(self.arm.need_calibration())
    #     self.assertIsNone(self.arm.reset_calibration())
    #     self.assertTrue(self.arm.need_calibration())
    #     self.assertTrue(self.arm.calibrate_auto())
    #     self.assertFalse(self.arm.need_calibration())
    #
    #     # Test Manual Calibration
    #     self.assertIsNone(self.arm.reset_calibration())
    #     self.assertTrue(self.arm.need_calibration())
    #     self.assertTrue(self.arm.calibrate(CalibrateMode.MANUAL))
    #     self.assertFalse(self.arm.need_calibration())
    #
    # def test_calibration_callback(self):
    #     calibration_event = Event()
    #     calibration_event.clear()
    #
    #     def callback_calibration_end(response):
    #         self.assertIsNotNone(response)
    #         calibration_event.set()
    #
    #     self.assertIsNone(self.arm.reset_calibration())
    #     self.assertTrue(self.arm.need_calibration())
    #
    #     self.assertIsNone(self.arm.calibrate_auto(callback=callback_calibration_end))
    #     self.assertTrue(calibration_event.wait(30))
    #     time.sleep(1)
    #     self.assertFalse(self.arm.need_calibration())


    # def test_request_new_calibration_callback(self):
    #     calibration_event = Event()
    #     calibration_event.clear()
    #
    #     def callback_calibration_end(response):
    #         self.assertIsNotNone(response)
    #         calibration_event.set()
    #
    #     self.assertTrue(self.arm.calibrate(CalibrateMode.MANUAL))
    #     self.assertFalse(self.arm.need_calibration())
    #
    #     self.assertIsNone(self.arm.request_new_calibration(callback=callback_calibration_end))
    #     self.assertTrue(self.arm.need_calibration())
    #     self.assertTrue(calibration_event.wait(30))
    #     time.sleep(1)
    #     self.assertFalse(self.arm.need_calibration())


    def test_learning_mode(self):

        def setter_learning_mode(state):
            self.arm.learning_mode = state

        self.assertTrue(self.arm.set_learning_mode(False))
        self.assertFalse(self.arm.learning_mode()['data'])

        self.assertTrue(self.arm.set_learning_mode(True))
        self.assertTrue(self.arm.learning_mode()['data'])

        self.assertIsNone(setter_learning_mode(False))
        self.assertFalse(self.arm.get_learning_mode())

        self.assertIsNone(setter_learning_mode(True))
        self.assertTrue(self.arm.get_learning_mode())

    def test_joints_state(self):
        self.arm.learning_mode = False
        self.assertAlmostEqualVector(self.arm.joints_state()["position"], self.arm.joints)
        self.assertAlmostEqualVector(self.arm.joints_state.value["position"], self.arm.get_joints())
        self.arm.learning_mode = True

    def test_pose_state(self):
        self.assertIsNotNone(self.arm.robot_pose())
        self.assertIsNotNone(self.arm.robot_pose.value)
        self.assertIsNotNone(self.arm.pose)
        self.assertIsNotNone(self.arm.get_pose())
        self.assertIsNotNone(self.arm.get_pose_quat())

    def test_move_joints(self):
        def setter_joints(joints):
            self.arm.joints = joints

        self.arm.set_learning_mode(False)

        self.assertIsNone(self.arm.move_joints(*(6*[0.2])))
        self.assertAlmostEqualVector(self.arm.joints, 6*[0.2])

        self.assertIsNone(self.arm.move_joints(6*[-0.2]))
        self.assertAlmostEqualVector(self.arm.joints, 6*[-0.2])

        self.assertIsNone(setter_joints([0, 0.5, -1.2, 0, 0, 0]))
        self.assertAlmostEqualVector(self.arm.get_joints(), [0, 0.5, -1.2, 0, 0, 0])

        with self.assertRaises(RobotCommandException):
            self.arm.move_joints(0.54, 0.964, 0.34, "a", "m", CalibrateMode.AUTO)

        self.arm.set_learning_mode(True)

        # Jog
        # self.assertIsNone(self.arm.jog_joints(0.1, -0.1, 0, 0, 0, 0))
        # time.sleep(0.75)
        # self.arm.set_jog_control(False)
        # self.assertAlmostEqualVector(self.arm.get_joints(), [0.1, -0.1, 0.0, 0.0, 0.0, 0.0])
        # Check Exception


    def test_pose(self):
        def setter_pose(pose):
            self.arm.pose = pose

        # Classic Move Pose & Get Pose
        self.assertIsNone(self.arm.move_pose(0.15, 0.0, 0.25, 0.0, 0.0, 0.0))
        self.assertIsNone(self.arm.move_pose([0.2, 0, 0.25, 0, 0, 0]))
        self.assertIsNone(setter_pose(PoseObject(0.2, 0, 0.3, 0, 0, 0)))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), [0.2, 0.0, 0.3, 0.0, 0.0, 0.0])
        self.assertAlmostEqualVector(self.arm.pose.to_list(), [0.2, 0.0, 0.3, 0.0, 0.0, 0.0])
        # Shift axis & Jog
        self.assertIsNone(self.arm.shift_pose(RobotAxis.Y, 0.05))
        self.assertIsNone(self.arm.jog_pose(-0.02, 0.0, 0.02, 0.1, 0, 0))
        self.arm.set_jog_control(False)
        # Check Exceptions
        with self.assertRaises(TcpCommandException):
            self.arm.shift_pose(ToolID.ELECTROMAGNET_1, 0.05)
        with self.assertRaises(TcpCommandException):
            self.arm.move_pose(0.54, 0.964, 0.34, "a", "m", CalibrateMode.AUTO)


if __name__ == '__main__':
    unittest.main()
