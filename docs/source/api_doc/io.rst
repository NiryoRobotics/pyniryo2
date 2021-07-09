I/Os
=====================================

I/Os - Command functions
------------------------------------

.. automodule:: pyniryo2.io.io
   :members:

This section reference all existing functions to control your robot, which include

- Getting IOs status
- Setting IOs mode
- Setting IOs value

All functions to control the robot are accessible via an instance of
the class :ref:`Niryo Robot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.io.set_pin_mode(PinID.GPIO_1A, PinMode.INPUT)
    robot.io.digital_write(PinID.GPIO_1A, PinState.HIGH)
    ...

See examples on :ref:`Examples Section <Examples: Conveyor>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1


State functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: IO
    :members: digital_io_states, get_digital_io_states, get_digital_io_state, set_pin_mode
    :member-order: bysource

Read & Write functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: IO
    :members: set_pin_mode, digital_write, digital_read
    :member-order: bysource


I/Os - Enums
------------------------------------

List of enums:

* :class:`pyniryo2.io.objects.PinMode`
* :class:`pyniryo2.io.objects.PinState`
* :class:`pyniryo2.io.objects.PinID`

.. automodule:: pyniryo2.io.enums
    :members:
    :undoc-members:
    :member-order: bysource

I/Os - Objects
------------------------------------

List of enums:

* :class:`pyniryo2.io.objects.DigitalPinObject`

.. automodule:: pyniryo2.io.objects
    :members:
    :undoc-members:
    :member-order: bysource
