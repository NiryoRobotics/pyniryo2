#!/usr/bin/env python
import time
import unittest
import roslibpy

from pyniryo2.exceptions import RobotCommandException

from pyniryo2.conveyor.enums import ConveyorID, ConveyorDirection
from pyniryo2.conveyor.conveyor import Conveyor
from pyniryo2.conveyor.topics import ConveyorInfo

robot_ip_address = "192.168.1.52"
port = 9090

test_order = ["test_conveyor_set_run",
              "test_bad_params_errors",
              ]


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = roslibpy.Ros(host=robot_ip_address, port=port)
        cls.client.run()
        cls.conveyor = Conveyor(cls.client)

    @classmethod
    def tearDownClass(cls):
        cls.client.terminate()


# noinspection PyTypeChecker
class TestConveyor(BaseTest):
    def test_conveyor_set_run(self):
        conveyor_id = self.conveyor.set_conveyor()
        self.assertIsInstance(conveyor_id, ConveyorID)

        self.assertIsInstance(self.conveyor.get_conveyors_feedback(), list)
        feedback = self.conveyor.get_conveyors_feedback()
        self.assertIsInstance(feedback[0], ConveyorInfo)
        self.assertEqual(feedback[0].conveyor_id, ConveyorID.ID_1)

        self.assertIsNone(self.conveyor.control_conveyor(ConveyorID.ID_1, True, 30, ConveyorDirection.BACKWARD))
        self.assertIsNone(time.sleep(1))
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0], ConveyorInfo(conveyor_id=ConveyorID.ID_1,
                                                                                 speed=30,
                                                                                 running=True,
                                                                                 direction=ConveyorDirection.BACKWARD))

        self.assertIsNone(self.conveyor.control_conveyor(ConveyorID.ID_1, True, 50, ConveyorDirection.FORWARD))
        self.assertIsNone(time.sleep(1))
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0], ConveyorInfo(conveyor_id=ConveyorID.ID_1,
                                                                                 speed=50,
                                                                                 running=True,
                                                                                 direction=ConveyorDirection.FORWARD))

        self.assertIsNone(self.conveyor.control_conveyor(ConveyorID.ID_1, False, 50, ConveyorDirection.FORWARD))
        self.assertIsNone(time.sleep(1))
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0], ConveyorInfo(conveyor_id=ConveyorID.ID_1,
                                                                                 speed=0,
                                                                                 running=False,
                                                                                 direction=ConveyorDirection.FORWARD))

        self.conveyor.run_conveyor(ConveyorID.ID_1)
        self.assertIsNone(time.sleep(1))
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0], ConveyorInfo(conveyor_id=ConveyorID.ID_1,
                                                                                 speed=100,
                                                                                 running=True,
                                                                                 direction=ConveyorDirection.FORWARD))

        self.conveyor.stop_conveyor(ConveyorID.ID_1)
        self.assertIsNone(time.sleep(1))
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].running, False)
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].speed, 0)

        self.assertIsNone(self.conveyor.unset_conveyor(ConveyorID.ID_1))
        self.assertEqual(self.conveyor.get_conveyors_feedback(), [])
        self.assertFalse(
            ConveyorID.ID_1 in [conveyor.conveyor_id for conveyor in self.conveyor.get_conveyors_feedback()])

        self.assertEqual(self.conveyor.set_conveyor(), ConveyorID.ID_1)

    def test_bad_params_errors(self):
        self.assertEqual(self.conveyor.set_conveyor(), ConveyorID.ID_1)

        with self.assertRaises(RobotCommandException):
            self.conveyor.unset_conveyor(1)

        with self.assertRaises(RobotCommandException):
            self.conveyor.control_conveyor(1, False, 50, ConveyorDirection.FORWARD)

        with self.assertRaises(RobotCommandException):
            self.conveyor.control_conveyor(ConveyorID, False, 50, ConveyorDirection.FORWARD)

        with self.assertRaises(RobotCommandException):
            self.conveyor.control_conveyor(ConveyorID.ID_1, 1, 50, ConveyorDirection.FORWARD)

        with self.assertRaises(RobotCommandException):
            self.conveyor.control_conveyor(ConveyorID.ID_1, True, -100, ConveyorDirection.FORWARD)

        with self.assertRaises(RobotCommandException):
            self.conveyor.control_conveyor(ConveyorID.ID_1, True, 200, ConveyorDirection.FORWARD)

        with self.assertRaises(RobotCommandException):
            self.conveyor.control_conveyor(ConveyorID.ID_1, True, 100, ConveyorDirection)

        with self.assertRaises(RobotCommandException):
            self.conveyor.control_conveyor(ConveyorID.ID_1, True, 100, 1)


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestConveyor(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
