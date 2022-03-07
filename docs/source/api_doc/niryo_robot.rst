NiryoRobot
=====================================

The NiryoRobot class includes the different APIs of the PyNiryo2 library.
It allows the connection of the program to the robot via roslibpy.
This interface facilitates and centralizes all the control functions of the Niryo environment and products.

NiryoRobot - Command functions
------------------------------------

.. automodule:: pyniryo2.niryo_robot
   :members:
   :noindex:

This section reference all existing functions of the NiryoRobot client, which include

- Connecting to your Ned
- Disconnecting from your Ned
- Waiting
- Access to the entire PyNiryo2 API

* :class:`~.niryo_robot.NiryoRobot`

All functions to control the robot are accessible via an instance of
the class :ref:`source/api_doc/niryo_robot:NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.run("10.10.10.10")
    robot.wait(2) # wait 2 seconds
    robot.end()

See examples on :ref:`Examples Section <source/examples/examples_basics:Examples: Basics>`


List of functions subsections:

.. contents::
   :local:
   :depth: 1


NiryoRobot functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: NiryoRobot
   :members: end, wait, client
   :member-order: bysource

NiryoRobot properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: NiryoRobot
   :members: arm, conveyor, io, pick_place, saved_poses, tool, trajectories, vision
   :member-order: bysource
   :noindex:


Globals Enums
------------------------------------

List of enums:

* :class:`~.enums.RobotErrors`
* :class:`~.enums.ArmMoveCommandType`

.. automodule:: pyniryo2.enums
    :members:
    :undoc-members:
    :member-order: bysource


Globals Objects
------------------------------------

* :class:`~.objects.PoseObject`

.. automodule:: pyniryo2.objects
    :members:
    :no-undoc-members:
    :member-order: bysource
    :noindex:
