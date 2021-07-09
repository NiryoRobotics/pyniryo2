Arm
=====================================

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
the class :ref:`Niryo Robot` ::


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
    :members: calibrate, calibrate_auto, request_new_calibration, reset_calibration, need_calibration,
    :member-order: bysource

Robot status functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Arm
    :members: hardware_status, joints_state, get_joints, joints, pose, get_pose, get_pose_quat
    :member-order: bysource

Learning mode functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Arm
    :members:  learning_mode, get_learning_mode, set_learning_mode,
    :member-order: bysource


Motion functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Arm
    :members: get_arm_max_velocity, set_arm_max_velocity,
              move_joints, move_pose, move_to_home_pose,
              move_linear_pose, stop_move, go_to_sleep,
              shift_pose, set_jog_control, jog_joints, jog_pose
    :member-order: bysource

Kinematics functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Arm
    :members: forward_kinematics, inverse_kinematics
    :member-order: bysource


Arm - Enums
------------------------------------

List of enums:

* :class:`~.arm.objects.CalibrateMode`
* :class:`~.arm.objects.RobotAxis`
* :class:`~.arm.objects.JogShift`

.. automodule:: arm.enums
    :members:
    :undoc-members:
    :member-order: bysource


Arm - Objects
------------------------------------

.. automodule:: arm.objects
    :members:
    :no-undoc-members:
    :member-order: bysource