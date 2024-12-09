Vision
=====================================

This file presents the different :ref:`api_doc/vision:Vision - Command functions`,
:ref:`api_doc/vision:Vision - Enums`, :ref:`api_doc/vision:Vision - Niryo Topics` & :ref:`api_doc/vision:Vision - NamedTuple` available with the Vision API


Vision - Command functions
------------------------------------

.. automodule:: pyniryo2.vision.vision
   :members:
   :noindex:


This section reference all existing functions to control your robot arm, which include

- Getting camera image
- Detecting objects
- Managing workspaces

All functions to control the robot are accessible via an instance of
the class :ref:`api_doc/niryo_robot:NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.vision.vision_pick("workspace_1", 0.0, ObjectShape.ANY, ObjectColor.ANY)
    robot.vision.detect_object("workspace_1", ObjectShape.ANY, ObjectColor.ANY)
    ...

See examples on :ref:`Examples Section <examples/examples_vision:Examples: Vision>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1


.. autoclass:: Vision


Camera functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoproperty:: Vision.get_img_compressed
.. autoproperty:: Vision.get_camera_intrinsics
.. autoproperty:: Vision.get_image_parameters
.. automethod:: Vision.set_brightness
.. automethod:: Vision.set_contrast
.. automethod:: Vision.set_saturation


Detection functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: Vision.get_target_pose_from_cam
.. automethod:: Vision.vision_pick
.. automethod:: Vision.move_to_object
.. automethod:: Vision.detect_object


Workspace functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: Vision.get_target_pose_from_rel
.. automethod:: Vision.save_workspace_from_robot_poses
.. automethod:: Vision.save_workspace_from_points
.. automethod:: Vision.delete_workspace
.. automethod:: Vision.get_workspace_ratio
.. automethod:: Vision.get_workspace_list


Vision - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`api_doc/niryo_topics:NiryoTopic` section.
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
      -  :exc:`list` [  :class:`numpy.uint8` ]
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
    :noindex:


Vision - Namedtuple
------------------------------------

.. automodule:: pyniryo2.vision.objects
    :members:
    :no-undoc-members:
    :member-order: bysource
    :noindex:
