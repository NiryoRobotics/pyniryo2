#!/usr/bin/env python
import unittest
import roslibpy
from threading import Event
import numpy as np

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_ros import NiryoRos
from pyniryo2.objects import PoseObject

from pyniryo2.trajectories.trajectories import Trajectories
from pyniryo2.arm.arm import Arm

robot_ip_address = "127.0.0.1"
port = 9090

test_order = ["test_creation_delete_trajectory",
              "test_save_trajectory_type",
              "test_execute_trajectory",
              "test_execute_trajectory_type",
              ]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = NiryoRos(ip_address=robot_ip_address, port=port)
        cls.trajectories = Trajectories(cls.client)
        cls.arm = Arm(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.arm.go_to_sleep()
        cls.client.close()

    @staticmethod
    def assertAlmostEqualVector(a, b, decimal=1):
        np.testing.assert_almost_equal(a, b, decimal)


# noinspection PyTypeChecker
class TestTrajectories(BaseTest):
    robot_poses = [[0.3, 0.1, 0.3, 0., 0., 0., 1.],
                   [0.3, -0.1, 0.3, 0., 0., 0., 1.],
                   [0.3, -0.1, 0.4, 0., 0., 0., 1.],
                   [0.3, 0.1, 0.4, 0., 0., 0., 1.]]

    neutral_pose = [0.2, 0.0, 0.4, 0., 0., 0.]

    def go_to_neutral_pose(self):
        self.assertIsNone(self.arm.move_pose(self.neutral_pose))
        self.assertAlmostEqualVector(self.arm.get_pose().to_list(), self.neutral_pose)

    def test_creation_delete_trajectory(self):
        # Get saved trajectory list & copy it
        self.assertIsInstance(self.trajectories.get_saved_trajectory_list(), list)
        traj_name_list = self.trajectories.get_saved_trajectory_list()

        # Create new trajectories
        list_names_saved = []
        for i in range(3):
            new_name = 'unittest_{:03d}'.format(i)
            self.assertIsNone(self.trajectories.save_trajectory(new_name, self.robot_poses))
            self.assertEqual(self.trajectories.get_trajectory_saved(new_name), self.robot_poses)
            if new_name not in traj_name_list:
                traj_name_list.append(new_name)
                list_names_saved.append(new_name)
            self.assertEqual(self.trajectories.get_saved_trajectory_list(), traj_name_list)

        # Delete created trajectories
        for name in list_names_saved:
            self.assertIsNone(self.trajectories.delete_trajectory(name))
            traj_name_list.pop(traj_name_list.index(name))
            self.assertEqual(self.trajectories.get_saved_trajectory_list(), traj_name_list)

            with self.assertRaises(RobotCommandException):
                self.assertIsNone(self.trajectories.delete_trajectory(name))

            with self.assertRaises(RobotCommandException):
                self.trajectories.get_trajectory_saved(name)

    def test_save_trajectory_type(self):
        traj_name = "unittest"
        if traj_name in self.trajectories.get_saved_trajectory_list():
            self.assertIsNone(self.trajectories.delete_trajectory(traj_name))

        self.trajectories.save_trajectory(traj_name, [[0.3, 0.1, 0.3, 0., 0., 0., 1.],
                                                      PoseObject(0.3, -0.1, 0.3, 0., 0., 0.),
                                                      [0.3, -0.1, 0.4, 0., 0., 0.],
                                                      PoseObject(0.3, 0.1, 0.4, 0., 0., 0.)])
        self.assertTrue(traj_name in self.trajectories.get_saved_trajectory_list())
        self.assertEqual(self.trajectories.get_trajectory_saved(traj_name), self.robot_poses)
        self.assertIsNone(self.trajectories.delete_trajectory(traj_name))
        self.assertFalse(traj_name in self.trajectories.get_saved_trajectory_list())

        with self.assertRaises(RobotCommandException):
            self.trajectories.save_trajectory(0, self.robot_poses)

        with self.assertRaises(RobotCommandException):
            self.trajectories.save_trajectory("unittest", [0.3, 0.1, 0.3, 0., 0., 0., 1.])

        with self.assertRaises(RobotCommandException):
            self.trajectories.save_trajectory("unittest", [[0.3, 0.1, 0.3, 0., 0.]])

    def test_execute_trajectory(self):
        # Testing trajectory from poses
        self.assertIsNone(self.arm.calibrate_auto())
        self.go_to_neutral_pose()
        self.assertIsNone(self.trajectories.execute_trajectory_from_poses(self.robot_poses))
        self.assertAlmostEqualVector(self.arm.get_pose().quaternion_pose, self.robot_poses[-1])

        trajectory_event = Event()
        trajectory_event.clear()

        def trajectory_callback(_):
            trajectory_event.set()

        self.go_to_neutral_pose()
        self.assertIsNone(
            self.trajectories.execute_trajectory_from_poses(self.robot_poses, dist_smoothing=0.05,
                                                            callback=trajectory_callback))
        self.assertTrue(trajectory_event.wait(20))
        self.assertAlmostEqualVector(self.arm.get_pose().quaternion_pose, self.robot_poses[-1])

        # Create & save a trajectory, then execute it & eventually delete it
        traj_name = "test_trajectory_save_and_execute"
        self.go_to_neutral_pose()
        self.assertIsNone(self.trajectories.save_trajectory(traj_name, self.robot_poses))
        self.assertIsNone(self.trajectories.execute_trajectory_saved(traj_name))
        self.assertAlmostEqualVector(self.arm.get_pose().quaternion_pose, self.robot_poses[-1])

        trajectory_event.clear()
        self.go_to_neutral_pose()
        self.assertIsNone(
            self.trajectories.execute_trajectory_saved(traj_name, dist_smoothing=0.02, callback=trajectory_callback))
        self.assertTrue(trajectory_event.wait(20))
        self.assertAlmostEqualVector(self.arm.get_pose().quaternion_pose, self.robot_poses[-1])
        self.assertIsNone(self.trajectories.delete_trajectory(traj_name))

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_saved(traj_name)

    def test_execute_trajectory_type(self):
        self.assertIsNone(self.arm.calibrate_auto())
        self.go_to_neutral_pose()
        self.trajectories.execute_trajectory_from_poses([[0.3, 0.1, 0.3, 0., 0., 0., 1.],
                                                         PoseObject(0.3, -0.1, 0.3, 0., 0., 0.),
                                                         [0.3, -0.1, 0.4, 0., 0., 0.],
                                                         PoseObject(0.3, 0.1, 0.4, 0., 0., 0.)])
        self.assertAlmostEqualVector(self.arm.get_pose().quaternion_pose, self.robot_poses[-1])

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_from_poses(0)

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_from_poses(PoseObject(0, 0, 0, 0, 0, 0))

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_from_poses([0.3, 0.1, 0.3, 0., 0., 0., 1.])

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_from_poses([[0.3, 0.1, 0.3, 0., 0.]])

        with self.assertRaises(RobotCommandException):
            self.trajectories.execute_trajectory_from_poses(self.robot_poses, dist_smoothing=-0.1)


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestTrajectories(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
