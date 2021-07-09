Conveyor
=====================================

This file presents the different :ref:`Conveyor - Command Functions`,
:ref:`Conveyor - Enums` & :ref:`Python Objects <Conveyor - Objects>` available with the API

Conveyor - Command Functions
------------------------------------

.. automodule:: pyniryo2.conveyor.conveyor
   :members:

.. autoclass:: Conveyor
    :members: set_conveyor, unset_conveyor, run_conveyor,
              stop_conveyor, control_conveyor, get_conveyors_feedback, conveyors
    :member-order: bysource

Conveyor - Enums
------------------------------------

List of enums:

* :class:`~.arm.objects.CalibrateMode`
* :class:`~.arm.objects.RobotAxis`
* :class:`~.arm.objects.JogShift`
* :class:`~.api.objects.ArmMoveCommandType`

.. automodule:: arm.enums
    :members:
    :undoc-members:
    :member-order: bysource

.. automodule:: enums
    :members:
    :undoc-members:
    :exclude-members: RobotErrors
    :member-order: bysource


Conveyor - Objects
------------------------------------

.. automodule:: conveyor.objects
    :members:
    :no-undoc-members:
    :member-order: bysource