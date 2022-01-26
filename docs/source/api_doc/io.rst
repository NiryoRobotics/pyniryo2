I/Os
=====================================

This file presents the different :ref:`I/Os - Command functions`,
:ref:`I/Os - Enums`, :ref:`I/Os - Niryo Topics` & :ref:`I/Os - Objects` available with the  Arm API


I/Os - Command functions
------------------------------------

.. automodule:: pyniryo2.io.io
   :members:
   :noindex:

This section reference all existing functions to control your robot, which include

- Getting IOs status
- Setting IOs mode
- Setting IOs value

All functions to control the robot are accessible via an instance of
the class :ref:`NiryoRobot` ::


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

.. autoproperty:: IO.digital_io_states
.. autoproperty:: IO.get_digital_io_states
.. automethod:: IO.get_digital_io_state


Read & Write functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: IO.set_pin_mode
.. automethod:: IO.digital_write
.. automethod:: IO.digital_read

I/Os - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`NiryoTopic` section.
They allow the acquisition of data in real time by callbacks or by direct call.

.. list-table:: I/O's Niryo Topics
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Function
      -  Return type
   *  -  ``/niryo_robot_rpi/digital_io_state``
      -  :attr:`~.io.IO.get_digital_io_states`
      -  :exc:`list` [ :class:`~.io.objects.DigitalPinObject` ]


I/Os - Enums
------------------------------------

List of enums:

* :class:`~.io.objects.PinMode`
* :class:`~.io.objects.PinState`
* :class:`~.io.objects.PinID`

.. automodule:: pyniryo2.io.enums
    :members:
    :undoc-members:
    :member-order: bysource
    :noindex:

I/Os - Objects
------------------------------------

.. automodule:: pyniryo2.io.objects
    :members:
    :undoc-members:
    :member-order: bysource
    :noindex:
