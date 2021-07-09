PyNiryo API Documentation
=====================================

This file presents the different :ref:`Command Functions`,
:ref:`Enums` & :ref:`Python Objects <Python Object classes>` available with the API

* :ref:`Command Functions` are used to deal directly the robot.
  It could be :meth:`~.api.tcp_client.NiryoRobot.move_joints`,
  :meth:`~.api.tcp_client.NiryoRobot.get_hardware_status`
  :meth:`~.api.tcp_client.NiryoRobot.vision_pick`, or also
  :meth:`~.api.tcp_client.NiryoRobot.run_conveyor`
* :ref:`Enums` are used to pass specific arguments to functions. For instance
  :class:`~.api.enums_communication.PinState`,
  :class:`~.api.enums_communication.ConveyorDirection`, ...
* :ref:`Python Objects <Python Object classes>`, as |pose_object|, ease some operations

Command Functions
------------------------------------
.. automodule:: arm.arm
   :members:
.. automodule:: conveyor.conveyor
   :members:
.. automodule:: io.io
   :members:
.. automodule:: pick_place.pick_place
   :members:
.. automodule:: saved_poses.saved_poses
   :members:
.. automodule:: tool.tool
   :members:
.. automodule:: trajectories.trajectories
   :members:
.. automodule:: vision.vision
   :members:

This section reference all existing functions to control your robot, which include

- Moving the robot
- Using Vision
- Controlling Conveyors
- Playing with Hardware

All functions to control the robot are accessible via an instance of
the class :class:`~.api.enums_communication.NiryoRobot` ::

    robot = NiryoRobot(<robot_ip_address>)

See examples on :ref:`Examples Section <Examples: Basics>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1

TCP Connection
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: NiryoRobot
    :members: run, end, wait

Main purpose functions
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Arm
    :members: calibrate, calibrate_auto, request_new_calibration, reset_calibration, need_calibration,
              hardware_status, learning_mode, get_learning_mode, set_learning_mode,
              get_arm_max_velocity, set_arm_max_velocity, wait
    :member-order: bysource

Joints & Pose
^^^^^^^^^^^^^

.. autoclass:: Arm
    :members: joints_state, joints, get_joints, pose, get_pose, get_pose_quat
              move_joints, move_pose, move_to_home_pose, go_to_sleep
              move_linear_pose, stop_move, go_to_sleep,
              shift_pose, set_jog_control, jog_joints, jog_pose, forward_kinematics, inverse_kinematics
    :member-order: bysource


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

Saved Poses
^^^^^^^^^^^^^

.. autoclass:: SavedPoses
    :members: get_pose_saved, save_pose, delete_pose, get_saved_pose_list
    :member-order: bysource

Pick & Place
^^^^^^^^^^^^^

.. autoclass:: PickPlace
    :members: pick_from_pose, place_from_pose, pick_and_place
    :member-order: bysource

Trajectories
^^^^^^^^^^^^^

.. autoclass:: Trajectories
    :members: get_trajectory_saved, execute_trajectory_from_poses, execute_trajectory_saved,
              save_trajectory, delete_trajectory, get_saved_trajectory_list
    :member-order: bysource

Tools
^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: tool, get_current_tool_id, update_tool, grasp_with_tool, release_with_tool,
              open_gripper, close_gripper, pull_air_vacuum_pump, push_air_vacuum_pump,
              setup_electromagnet, activate_electromagnet, deactivate_electromagnet
    :member-order: bysource

IO
^^^^^^^^^^^^^

.. autoclass:: IO
    :members: digital_io_states, get_digital_io_states, get_digital_io_state,
              set_pin_mode, digital_write, digital_read
    :member-order: bysource

Conveyor
^^^^^^^^^^^^^

.. autoclass:: Conveyor
    :members: set_conveyor, unset_conveyor, run_conveyor,
              stop_conveyor, control_conveyor, get_conveyors_feedback, conveyors
    :member-order: bysource

Vision
^^^^^^^^^^^^^

.. autoclass:: Vision
    :members: get_img_compressed, get_target_pose_from_rel, get_target_pose_from_cam,
              vision_pick, move_to_object, detect_object, get_camera_intrinsics,
              save_workspace_from_robot_poses, save_workspace_from_points,
              delete_workspace, get_workspace_ratio, get_workspace_list
    :member-order: bysource


Python Object classes
------------------------------------

.. automodule:: objects
    :members:
    :no-undoc-members:
    :member-order: bysource

.. automodule:: arm.objects
    :members:
    :no-undoc-members:
    :member-order: bysource

.. |pose_object| replace:: :class:`~.api.objects.PoseObject`
.. |hardware_status_object| replace:: :class:`~.arm.objects.HardwareStatusObject`
.. |joint_state_object| replace:: :class:`~.arm.objects.JointStateObject`