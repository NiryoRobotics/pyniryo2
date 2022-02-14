Conveyor
=====================================

This file presents the different :ref:`source/api_doc/conveyor:Conveyor - Command functions`,
:ref:`source/api_doc/conveyor:Conveyor - Enums`, :ref:`source/api_doc/conveyor:Conveyor - Niryo Topics` & :ref:`source/api_doc/conveyor:Conveyor - Namedtuple` available with the  Arm API


Conveyor - Command functions
------------------------------------

.. automodule:: pyniryo2.conveyor.conveyor
   :members:
   :noindex:

This section reference all existing functions to control your robot, which include

- Controlling conveyors

All functions to control the robot are accessible via an instance of
the class :ref:`source/api_doc/niryo_robot:NiryoRobot` ::

    robot = NiryoRobot(<robot_ip_address>)

    conveyor_id = robot.conveyor.set_conveyor()
    robot.conveyor.run_conveyor(conveyor_id)
    ...

See examples on :ref:`Examples Section <source/examples/examples_conveyor:Examples: Conveyor>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1

Conveyor functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Conveyor
    :members: set_conveyor, unset_conveyor, run_conveyor,
              stop_conveyor, control_conveyor, get_conveyors_feedback, conveyors
    :member-order: bysource

Conveyor - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`source/api_doc/niryo_topics:NiryoTopic` section.
They allow the acquisition of data in real time by callbacks or by direct call.

.. list-table:: Conveyors's Niryo Topics
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Function
      -  Return type
   *  -  ``/niryo_robot/conveyor/feedback``
      -  :attr:`~.conveyor.Conveyor.get_conveyors_feedback`
      -  :exc:`list` [ :class:`~.conveyor.objects.ConveyorInfo` ]

Conveyor - Enums
------------------------------------

List of enums:

* :class:`~.conveyor.objects.ConveyorID`
* :class:`~.conveyor.objects.ConveyorDirection`
* :class:`~.conveyor.objects.ConveyorStatus`

.. automodule:: pyniryo2.conveyor.enums
    :members:
    :undoc-members:
    :exclude-members:
    :member-order: bysource
    :noindex:


Conveyor - Namedtuple
------------------------------------

.. automodule:: pyniryo2.conveyor.objects
    :members:
    :no-undoc-members:
    :member-order: bysource
    :noindex:
