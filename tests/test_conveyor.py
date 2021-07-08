#!/usr/bin/env python
import unittest
import roslibpy
from threading import Event

from pyniryo2.exceptions import RobotCommandException
from pyniryo2.niryo_topic import NiryoTopic
from pyniryo2.enums import RobotErrors

from pyniryo2.conveyor.enums import ConveyorID, ConveyorDirection, ConveyorStatus
from pyniryo2.conveyor.conveyor import Conveyor


robot_ip_address = "192.168.1.118"
port = 9090

test_order = ["test_conveyor_feedback"]
              # "test_update_conveyor",
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
    def test_conveyor_feeback(self):
        self.assertIsNone(time.sleep(1))
        self.assertIsInstance(self.conveyor.get_conveyors_feedback, NiryoTopic)
        self.assertIsInstance(self.conveyor.get_conveyors_feedback(), namedTuple)
        self.assertIsInstance(self.conveyor.get_conveyors_feedback.conveyor_id, int)
        self.assertIsInstance(self.conveyor.get_conveyors_feedback.connection_state, bool)
        self.assertIsInstance(self.conveyor.get_conveyors_feedback.running, bool)
        self.assertIsInstance(self.conveyor.get_conveyors_feedback.speed, int)
        self.assertIsInstance(self.conveyor.get_conveyors_feedback.direction, int)

def suite():
    suite = unittest.TestSuite()
    for function_name in test_order:
        suite.addTest(TestConveyor(function_name))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
