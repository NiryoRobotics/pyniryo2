#!/usr/bin/env python
import time
import unittest
import roslibpy
import numpy as np
from threading import Event

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_topic import NiryoTopic
from pyniryo2.enums import RobotErrors
from pyniryo2.io.enums import PinID
from pyniryo2.vision.vision import Vision
from pyniryo2.vision.topics import CameraInfo
from pyniryo2.objects import PoseObject

robot_ip_address = "192.168.1.52"
port = 9090

test_order = ["test_camera_info",
              "test_camera_img",
                "test_workspace",
              ]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = roslibpy.Ros(host=robot_ip_address, port=port)
        cls.client.run()
        cls.vision = Vision(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.terminate()

    @staticmethod
    def assertAlmostEqualVector(a, b, decimal=1):
        np.testing.assert_almost_equal(a, b, decimal)


# noinspection PyTypeChecker
class TestVision(BaseTest):

    def test_camera_info(self):
        self.assertIsInstance(self.vision.get_camera_intrinsics, NiryoTopic)
        self.assertIsInstance(self.vision.get_camera_intrinsics(), CameraInfo)

        cam_event = Event()
        cam_event.clear()

        def camera_info_callback(cam_info):
            self.assertIsInstance(cam_info, CameraInfo)
            cam_event.set()

        self.assertIsNone(self.vision.get_camera_intrinsics.subscribe(camera_info_callback))
        self.assertTrue(cam_event.wait(10))
        self.assertIsNone(self.vision.get_camera_intrinsics.unsubscribe())

    def test_camera_img(self):
        self.assertIsInstance(self.vision.get_img_compressed, NiryoTopic)
        self.assertIsInstance(self.vision.get_img_compressed(), str)

        cam_event = Event()
        cam_event.clear()

        def camera_img_callback(img):
            self.assertIsInstance(img, str)
            cam_event.set()

        self.assertIsNone(self.vision.get_img_compressed.subscribe(camera_img_callback))
        self.assertTrue(cam_event.wait(10))
        self.assertIsNone(self.vision.get_img_compressed.unsubscribe())

    def test_workspace(self):
        ws_name = "unit_test_ws"
        self.assertIsNone(self.vision.delete_workspace(ws_name))

        unit_test_ws_poses = [ws_name,
                              [0.3, -0.1, 0.0, 0.0, 1.57, 0.0],
                              PoseObject(0.3, 0.1, 0.0, 0.0, 1.57, 0.0),
                              PoseObject(0.1, 0.1, 0.0, 0.0, 1.57, 0.0),
                              [0.1, -0.1, 0.0, 0.0, 1.57, 0.0]]

        unit_test_ws_points = [ws_name,
                               [0.3, -0.1, 0.0],
                               [0.3, 0.1, 0.0],
                               [0.2, 0.1, 0.0],
                               [0.2, -0.1, 0.0]]

        self.assertIsNone(self.vision.save_workspace_from_robot_poses(*unit_test_ws_poses))
        self.assertTrue(ws_name in self.vision.get_workspace_list())
        self.assertAlmostEquals(self.vision.get_workspace_ratio(ws_name), 1.0, places=2)
        # with self.assertRaises(RobotCommandException):
        #     self.vision.save_workspace_from_robot_poses(*unit_test_ws_poses)

        self.assertIsNone(self.vision.delete_workspace(ws_name))
        self.assertFalse(ws_name in self.vision.get_workspace_list())

        self.assertIsNone(self.vision.save_workspace_from_points(*unit_test_ws_points))
        self.assertTrue(ws_name in self.vision.get_workspace_list())
        self.assertAlmostEquals(self.vision.get_workspace_ratio(ws_name), 2.0, places=2)

        test_poses = self.vision.get_workspace_poses(ws_name)
        for pose_obtained, pose_expected in zip(test_poses, unit_test_ws_poses[0:]):
            self.assertAlmostEqualVector(pose_obtained, pose_expected.to_list()[:3], decimal=3)

        self.assertIsNone(self.vision.delete_workspace(ws_name))
        self.assertFalse(ws_name in self.vision.get_workspace_list())


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestVision(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
