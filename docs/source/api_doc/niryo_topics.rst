NiryoTopic
=====================================

Pyniryo2 is based on the python library roslibpy to collect information from the robot.
This information is sent by ROS via topics. This class is an overlay of the API
`roslibpy Topic <https://roslibpy.readthedocs.io/en/latest/reference/index.html#topics>`_.
It allows you to subscribe to a topic to collect the information from the topic as soon as it is published,
or ask for only one value.
Please refer to the Niryo robot ROS doc to see the compatible topics.

NiryoTopic - Usage
------------------------------------

.. automodule:: pyniryo2.niryo_topic
   :members:
   :noindex:

Here is a simple example of using the class without conversion: ::


    >> robot = NiryoRobot(<robot_ip_address>)
    >> client = robot.client
    >> joint_states_topic = NiryoTopic(client, '/joint_states', 'sensor_msgs/JointState')
    >> joint_states_topic()
    {u'header': {u'stamp': {u'secs': 1626092430, u'nsecs': 945618510}, u'frame_id': u'', u'seq': 13699},
    u'position': [0.0, 0.6, -1.3, 0.0, 0.0, 0.0], u'effort': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    u'name': [u'joint_1', u'joint_2', u'joint_3', u'joint_4', u'joint_5', u'joint_6'],
    u'velocity': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}


Here is a simple example of using the class with conversion: ::

    >> def joint_states_topic_conversion(msg):
            return msg["position"]

    >> robot = NiryoRobot(<robot_ip_address>)
    >> client = robot.client
    >> joint_states_topic = NiryoTopic(client, '/joint_states', 'sensor_msgs/JointState', joint_states_topic_conversion)
    >> joint_states_topic()
    [0.0, 0.6, -1.3, 0.0, 0.0, 0.0]
    >> joint_states_topic.value
    [0.0, 0.6, -1.3, 0.0, 0.0, 0.0]

Here is a simple example of using the class with a callback: ::

    def joint_states_topic_conversion(msg):
        return msg["position"]

    def joint_states_callback(msg):
        print(msg) # print the list of joints position

    robot = NiryoRobot("127.0.0.1")
    client = robot.client
    joint_states_topic = NiryoTopic(client, '/joint_states', 'sensor_msgs/JointState', joint_states_topic_conversion)
    joint_states_topic.subscribe(joint_states_callback)

    ...

    joint_states_topic.unsubscribe()


NiryoTopic - Class
------------------------------------

* :class:`~.niryo_topic.NiryoTopic`

.. automethod:: NiryoTopic.subscribe
.. automethod:: NiryoTopic.unsubscribe
.. autoproperty:: NiryoTopic.value
.. autoproperty:: NiryoTopic.is_subscribed
