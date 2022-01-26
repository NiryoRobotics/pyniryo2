Trajectories
=====================================

This file presents the different :ref:`Trajectories - Command functions` available with the Trajectories API


Trajectories - Command functions
------------------------------------

.. automodule:: pyniryo2.trajectories.trajectories
   :members:
   :noindex:

This section reference all existing functions to control your robot, which include

- Playing smoothed waypointed trajectories
- Managing saved trajectories

All functions to control the robot are accessible via an instance of
the class :ref:`NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    trajectories = robot.trajectories.get_saved_trajectory_list()
    if len(trajectories) > 0:
        robot.trajectories.execute_trajectory_saved(trajectories[0])
    ...

See examples on :ref:`Examples Section <Examples: Movement>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1

Trajectories functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Trajectories
    :members: get_trajectory_saved, execute_trajectory_from_poses, execute_trajectory_saved,
              save_trajectory, delete_trajectory, get_saved_trajectory_list
    :member-order: bysource


