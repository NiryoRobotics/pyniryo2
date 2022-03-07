Arm
=====================================

This file presents the different :ref:`source/api_doc/arm:Arm - Command functions`,
:ref:`source/api_doc/arm:Arm - Enums`, :ref:`source/api_doc/arm:Arm - Niryo Topics` & :ref:`source/api_doc/arm:Arm - Objects` available with the  Arm API

Arm - Command functions
------------------------------------

.. automodule:: pyniryo2.arm.arm
   :members:
   :noindex:


This section reference all existing functions to control your robot arm, which include

- Getting the robot state
- Moving the arm
- Getting inverse and forward kinematics
- Calibrating the robot

All functions to control the robot are accessible via an instance of
the class :ref:`source/api_doc/niryo_robot:NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.arm.calibrate_auto()
    robot.arm.move_joints([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    ...

See examples on :ref:`Examples Section <source/examples/examples_basics:Examples: Basics>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1

.. autoclass:: Arm


Calibration functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: Arm.calibrate
.. automethod:: Arm.calibrate_auto
.. automethod:: Arm.request_new_calibration
.. automethod:: Arm.reset_calibration
.. automethod:: Arm.need_calibration


Robot status functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoproperty:: Arm.hardware_status
.. autoproperty:: Arm.joints_state
.. automethod:: Arm.get_joints
.. autoproperty:: Arm.joints
.. autoproperty:: Arm.pose
.. autoproperty:: Arm.get_pose
.. automethod:: Arm.get_pose_quat


Learning mode functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoproperty:: Arm.learning_mode
.. automethod:: Arm.get_learning_mode
.. automethod:: Arm.set_learning_mode


Kinematics functions
^^^^^^^^^^^^^^^^^^^^

.. automethod:: Arm.forward_kinematics
.. automethod:: Arm.inverse_kinematics


Arm - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`source/api_doc/niryo_topics:NiryoTopic` section.
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
    :noindex:

Arm - Objects
------------------------------------

* :class:`HardwareStatusObject`

.. autoclass:: pyniryo2.arm.objects.HardwareStatusObject


* :class:`JointStateObject`

.. autoclass:: pyniryo2.arm.objects.JointStateObject

* :class:`~.objects.PoseObject`

.. autoclass:: pyniryo2.objects.PoseObject
