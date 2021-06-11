#!/usr/bin/env python

import numpy as np
import sys
import unittest
import roslibpy
from threading import Event

from pyniryo2.niryo_topic import NiryoTopic
from pyniryo2.exceptions import TopicException

simulation = "-simu" in sys.argv

robot_ip_address_rpi = "192.168.1.52"
robot_ip_address_gazebo = "127.0.0.1"
robot_ip_address = robot_ip_address_gazebo if simulation else robot_ip_address_rpi
port = 9090


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = roslibpy.Ros(host=robot_ip_address, port=port)
        cls.client.run()

    @classmethod
    def tearDownClass(cls):
        cls.client.terminate()

    @staticmethod
    def assertAlmostEqualVector(a, b, decimal=1):
        np.testing.assert_almost_equal(a, b, decimal)


# noinspection PyTypeChecker
class TestTopic(BaseTest):

    def setUp(self):
        self.topic_name = '/joint_states'
        self.topic_type = 'sensor_msgs/JointState'

    def test_subscribe_unsubscribe(self):
        self.topic_message = None
        self.message_event = Event()
        self.message_event.clear()

        def callback(message):
            self.topic_message = message
            self.message_event.set()

        topic = NiryoTopic(self.client, self.topic_name, self.topic_type)

        self.assertFalse(topic.is_subscribed)

        # Try a bad subscription
        with self.assertRaises(TopicException):
            topic.subscribe(None)

        # Subscribe
        self.assertIsNone(topic.subscribe(callback))
        self.assertTrue(topic.is_subscribed)

        # Wait a message
        self.assertTrue(self.message_event.wait(timeout=0.5))
        self.assertIsNotNone(self.topic_message)

        # Unsubscibe
        self.assertIsNone(topic.unsubscribe())
        self.assertFalse(topic.is_subscribed)

    def test_synchronous_access(self):
        self.assertTrue(self.client.is_connected)

        topic = NiryoTopic(self.client, self.topic_name, self.topic_type)
        self.assertFalse(topic.is_subscribed)

        # Wait a message
        message = topic()
        self.assertIsNotNone(message)
        self.assertNotEqual(message, topic())

        self.assertFalse(topic.is_subscribed)

    def test_synchronous_with_asynchronous_access(self):
        self.topic_message = None
        self.message_event = Event()
        self.message_event.clear()

        def callback(message):
            self.assertEqual(topic(), message)
            self.topic_message = message
            self.message_event.set()

        topic = NiryoTopic(self.client, self.topic_name, self.topic_type)

        # Synchronous access
        self.assertIsNotNone(topic())
        self.assertFalse(topic.is_subscribed)

        # Subscribe
        self.assertIsNone(topic.subscribe(callback))
        self.assertTrue(topic.is_subscribed)

        # Wait a message
        self.assertTrue(self.message_event.wait(timeout=0.5))
        self.assertIsNotNone(self.topic_message)

        # Unsubscibe
        self.assertIsNone(topic.unsubscribe())
        self.assertFalse(topic.is_subscribed)


if __name__ == '__main__':
    unittest.main()
