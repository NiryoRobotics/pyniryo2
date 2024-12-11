Frames
=====================================

This file presents the different :ref:`api_doc/frames:Frames - Command functions` available with the Frames API

All functions to control the robot are accessible via an instance of
the class :ref:`api_doc/niryo_robot:NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    frames = frames.get_saved_dynamic_frame_list()
    ...

Frames - Command functions
------------------------------------

.. automodule:: pyniryo2.frames.frames
   :members:
   :noindex:


List of functions subsections:

.. contents::
   :local:
   :depth: 1

Frames functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Frames
    :members: get_saved_dynamic_frame_list, get_saved_dynamic_frame, 
     save_dynamic_frame_from_poses, save_dynamic_frame_from_points, 
     edit_dynamic_frame, delete_saved_dynamic_frame
    :member-order: bysource
