Pick & Place
=====================================

This file presents the different :ref:`api_doc/pick_place:Pick & Place - Command functions` available with the Pick & Place API


Pick & Place - Command functions
------------------------------------

.. automodule:: pyniryo2.pick_place.pick_place
   :members:
   :noindex:

This section reference all existing functions to control your robot, which include

- Picking objects
- Placing objects


All functions to control the robot are accessible via an instance of
the class :ref:`api_doc/niryo_robot:NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.pick_place.pick_from_pose([0.2, 0.0, 0.1, 0.0, 1.57, 0.0])
    robot.pick_place.place_from_pose([0.0, 0.2, 0.1, 0.0, 1.57, 0.0])
    ...

See examples on :ref:`Examples Section <examples/examples_vision:Examples: Vision>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1


Pick & Place functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: PickPlace
    :members: pick_from_pose, place_from_pose, pick_and_place
    :member-order: bysource


