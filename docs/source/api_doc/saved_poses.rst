Saved poses
=====================================

Saved poses - Command functions
------------------------------------

.. automodule:: pyniryo2.saved_poses.saved_poses
   :members:

This section reference all existing functions to control your robot, which include

- Managing of saved poses

All functions to control the robot are accessible via an instance of
the class :ref:`Niryo Robot` ::


    robot = NiryoRobot(<robot_ip_address>)

    pose_name_list = robot.saved_poses.get_saved_pose_list()
    robot.saved_poses.get_pose_saved(pose_name_list[0])
    ...

See examples on :ref:`Examples Section <Examples: Conveyor>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1

Saved poses functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: SavedPoses
    :members: get_pose_saved, save_pose, delete_pose, get_saved_pose_list
    :member-order: bysource
