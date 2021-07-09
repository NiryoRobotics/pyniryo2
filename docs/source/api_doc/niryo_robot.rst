NiryoRobot
=====================================



NiryoRobot - Command functions
------------------------------------

.. automodule:: pyniryo2.niryo_robot
   :members:

This section reference all existing functions of the NiryoRobot client, which include

- Connecting to your Ned
- Disconnecting from your Ned
- Waiting

All functions to control the robot are accessible via an instance of
the class NiryoRobot ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.run("10.10.10.10")
    robot.wait(2) # wait 2 seconds
    robot.end()

See examples on :ref:`Examples Section <Examples: Basics>`


List of functions subsections:

.. contents::
   :local:
   :depth: 1


NiryoRobot functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :class:`~.niryo_robot.NiryoRobot`

.. autoclass:: NiryoRobot2
    :members: run, end, wait
    :member-order: bysource


Globals Enums
------------------------------------

List of enums:

* :class:`~.objects.RobotErrors`

.. automodule:: enums
    :members:
    :undoc-members:
    :member-order: bysource


Globals Objects
------------------------------------

* :class:`~.objects.PoseObject`

.. automodule:: objects
    :members:
    :no-undoc-members:
    :member-order: bysource