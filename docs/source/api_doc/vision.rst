Vision
=====================================

This file presents the different :ref:`Vision - Command functions`,
:ref:`Vision - Enums`, :ref:`Vision - Niryo Topics` & :ref:`Vision - NamedTuple` available with the Vision API


Vision - Command functions
------------------------------------

.. automodule:: pyniryo2.vision.vision
   :members:


This section reference all existing functions to control your robot arm, which include

- Getting camera image
- Detecting objects
- Managing workspaces

All functions to control the robot are accessible via an instance of
the class :ref:`NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.vision.vision_pick("workspace_1", 0.0, ObjectShape.ANY, ObjectColor.ANY)
    robot.vision.detect_object("workspace_1", ObjectShape.ANY, ObjectColor.ANY)
    ...

See examples on :ref:`Examples Section <Examples: Vision>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1


Camera functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Vision
    :members: get_img_compressed, get_camera_intrinsics
    :member-order: bysource

Detection functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Vision
    :members: get_target_pose_from_cam, vision_pick, move_to_object, detect_object
    :member-order: bysource


Workspace functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Vision
    :members: get_target_pose_from_rel, save_workspace_from_robot_poses, save_workspace_from_points,
              delete_workspace, get_workspace_ratio, get_workspace_list
    :member-order: bysource


Vision - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`NiryoTopic` section.
They allow the acquisition of data in real time by callbacks or by direct call.

.. list-table:: Vision's Niryo Topics
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Function
      -  Return type
   *  -  ``/niryo_robot_vision/compressed_video_stream``
      -  :attr:`~.vision.Vision.get_img_compressed`
      -  :exc:`list` [  :numpy_type:`numpy.uint8` ]
   *  -  ``/niryo_robot_vision/camera_intrinsics``
      -  :attr:`~.vision.Vision.get_camera_intrinsics`
      -  :class:`~.vision.objects.CameraInfo`

Vision - Enums
------------------------------------

List of enums:

* :class:`~.vision.enums.ObjectColor`
* :class:`~.vision.enums.ObjectShape`
* :class:`~.vision.enums.ManageWorkspace`

.. automodule:: pyniryo2.vision.enums
    :members:
    :undoc-members:
    :member-order: bysource


Vision - Namedtuple
------------------------------------

.. automodule:: pyniryo2.vision.objects
    :members:
    :no-undoc-members:
    :member-order: bysourceclass
