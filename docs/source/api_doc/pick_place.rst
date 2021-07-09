Pick & Place
=====================================

Pick & Place - Command functions
------------------------------------

.. automodule:: pyniryo2.pick_place.pick_place
   :members:

This section reference all existing functions to control your robot, which include

- Picking objects
- Placing objects


All functions to control the robot are accessible via an instance of
the class :ref:`Niryo Robot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.io.set_pin_mode(PinID.GPIO_1A, PinMode.INPUT)
    robot.io.digital_write(PinID.GPIO_1A, PinState.HIGH)
    ...

See examples on :ref:`Examples Section <Examples: Vision>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1


Pick & Place functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: PickPlace
    :members: pick_from_pose, place_from_pose, pick_and_place
    :member-order: bysource


