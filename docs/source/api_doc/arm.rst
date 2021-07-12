Arm
=====================================

This file presents the different :ref:`Arm - Command functions`,
:ref:`Arm - Enums`, :ref:`Arm - Niryo Topics` & :ref:`Arm - Objects` available with the  Arm API

Arm - Command functions
------------------------------------

.. automodule:: pyniryo2.arm.arm
   :members:


This section reference all existing functions to control your robot arm, which include

- Getting the robot state
- Moving the arm
- Getting inverse and forward kinematics
- Calibrating the robot

All functions to control the robot are accessible via an instance of
the class :ref:`NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.arm.calibrate_auto()
    robot.arm.move_joints([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    ...

See examples on :ref:`Examples Section <Examples: Basics>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1


Calibration functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Arm
    :members: calibrate, calibrate_auto, request_new_calibration, reset_calibration, need_calibration
    :member-order: bysource


Robot status functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Arm
    :members: hardware_status, joints_state, get_joints, joints, pose, get_pose, get_pose_quat
    :member-order: bysource


Learning mode functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Arm
    :members:  learning_mode, get_learning_mode, set_learning_mode
    :member-order: bysource


Kinematics functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Arm
    :members: forward_kinematics, inverse_kinematics
    :member-order: bysource


Arm - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`NiryoTopic` section.
They allow the acquisition of data in real time by callbacks or by direct call.

.. list-table:: Arm's Niryo Topics
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Function
      -  Return type
   *  -  ``/joint_states``
      -  :attr:`~.arm.Arm.joints_state`
      -  :class:`~.arm.objects.JointStateObject`
   *  -  ``/niryo_robot/robot_state``
      -  :attr:`~.arm.Arm.get_pose`
      -  :class:`~.objects.PoseObject`
   *  -  ``/niryo_robot_hardware_interface/hardware_status``
      -  :attr:`~.arm.Arm.hardware_status`
      -  :class:`~.arm.objects.HardwareStatusObject`
   *  -  ``/niryo_robot/learning_mode/state``
      -  :attr:`~.arm.Arm.learning_mode`
      -  :exc:`bool`
   *  -  ``/niryo_robot/max_velocity_scaling_factor``
      -  :attr:`~.arm.Arm.get_arm_max_velocity`
      -  :exc:`float`

Arm - Enums
------------------------------------

List of enums:

* :class:`~.arm.enums.CalibrateMode`
* :class:`~.arm.enums.RobotAxis`
* :class:`~.arm.enums.JogShift`

.. automodule:: pyniryo2.arm.enums
    :members:
    :undoc-members:
    :member-order: bysource


Arm - Objects
------------------------------------

.. automodule:: pyniryo2.arm.objects
    :members:
    :no-undoc-members:
    :member-order: bysource