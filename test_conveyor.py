#!/usr/bin/env python
import time
from collections import namedtuple
import unittest
import roslibpy
from threading import Event

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_topic import NiryoTopic
from pyniryo2.enums import RobotErrors

from pyniryo2.conveyor.enums import ConveyorID, ConveyorDirection, ConveyorStatus
from pyniryo2.conveyor.conveyor import Conveyor
from pyniryo2.conveyor.topics import ConveyorInfo


robot_ip_address = "192.168.1.118"
port = 9090

test_order = ["test_conveyor_variable",
              "test_conveyor_set_run"]
              # "test_run_conveyor",
              # "test_control_conveyor",
              # "test_shutdown_conveyor"]


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
    def test_conveyor_variable(self):
        self.assertIsNone(time.sleep(1))
        self.assertIsInstance(self.conveyor.get_conveyors_feedback, NiryoTopic)
        self.assertIsInstance(self.conveyor.set_conveyor(), int)
        conveyor_id = self.conveyor.set_conveyor()
        self.assertIsInstance(self.conveyor.unset_conveyor(conveyor_id), tuple)
        self.assertIsInstance(self.conveyor.unset_conveyor(conveyor_id)[0], str)
        self.assertIsInstance(self.conveyor.unset_conveyor(conveyor_id)[1], str)
        self.assertIsNone(self.conveyor.run_conveyor(conveyor_id), None)
        self.assertIsInstance(self.conveyor.control_conveyor(conveyor_id, True, 30, ConveyorDirection.BACKWARD.value), tuple)
        self.assertIsInstance(self.conveyor.control_conveyor(conveyor_id, True, 100, ConveyorDirection.BACKWARD.value)[0], str)
        self.assertIsInstance(self.conveyor.control_conveyor(conveyor_id, True, 50, ConveyorDirection.FORWARD.value)[1], str)
    
    def test_conveyor_set_run(self):
        self.assertIsNone(time.sleep(1))
        self.assertTrue(self.conveyor.set_conveyor())
        self.assertIsNone(time.sleep(1))
        conveyor_id = self.conveyor.set_conveyor()


        # ---- Uncomment second line if conveyor plugged with ID_2 ----
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].conveyor_id, ConveyorID.ID_1.value)
        # self.assertEqual(self.conveyor.get_conveyors_feedback()[0].conveyor_id, ConveyorID.ID_2.value)
        self.assertIsNone(time.sleep(2))

        self.assertEqual(int(self.conveyor.control_conveyor(conveyor_id, True, 30, ConveyorDirection.BACKWARD.value)[0]), 1) # 1 --> runnung
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].direction, ConveyorDirection.BACKWARD.value)
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].speed, 30)
        self.assertIsNone(time.sleep(2))

        self.assertEqual(int(self.conveyor.control_conveyor(conveyor_id, True, 100, ConveyorDirection.FORWARD.value)[0]), 1) # 1 --> running
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].direction, ConveyorDirection.FORWARD.value)
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].speed, 100)
        self.assertIsNone(time.sleep(2))

        self.conveyor.stop_conveyor(conveyor_id)
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].direction, ConveyorDirection.FORWARD.value)
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].speed, 0)
        self.assertIsNone(time.sleep(2))

        self.conveyor.run_conveyor(conveyor_id) 
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].direction, ConveyorDirection.FORWARD.value)
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].speed, 50)
        self.assertIsNone(time.sleep(2))
        self.conveyor.stop_conveyor(conveyor_id)

        self.conveyor.unset_conveyor(conveyor_id)
        self.assertEqual(self.conveyor.get_conveyors_feedback(), [])
        self.conveyor.set_conveyor()
        self.assertEqual(self.conveyor.get_conveyors_feedback()[0].conveyor_id, ConveyorID.ID_1.value)


def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestConveyor(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
