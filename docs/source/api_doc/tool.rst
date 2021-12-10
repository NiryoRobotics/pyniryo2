Tool
=====================================

This file presents the different :ref:`Tool - Command functions`,
:ref:`Tool - Enums` & :ref:`Tool - Niryo Topics` available with the Tool API


Tool - Command Functions
------------------------------------

.. automodule:: pyniryo2.tool.tool
   :members:


This section reference all existing functions to control your robot, which include

- Using tools
- Using grippers
- Using the vacuum pump
- Using the electromagnet
- Management of the TCP

All functions to control the robot are accessible via an instance of
the class :ref:`NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.tool.update_tool()
    robot.tool.grasp_with_tool()
    robot.tool.release_with_tool()
    ...

See examples on :ref:`Examples Section <Examples: Tool Action>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1


Tool functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: update_tool, tool, get_current_tool_id, grasp_with_tool, release_with_tool
    :member-order: bysource

Grippers functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: open_gripper, close_gripper
    :member-order: bysource

Vacuum pump functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: pull_air_vacuum_pump, push_air_vacuum_pump
    :member-order: bysource

Electromagnet functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: setup_electromagnet, activate_electromagnet, deactivate_electromagnet
    :member-order: bysource

TCP functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: enable_tcp, set_tcp, reset_tcp
    :member-order: bysource

Tool - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`NiryoTopic` section.
They allow the acquisition of data in real time by callbacks or by direct call.

.. list-table:: Tool's Niryo Topics
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Function
      -  Return type
   *  -  ``/niryo_robot_tools_commander/current_id``
      -  :attr:`~.tool.Tool.get_current_tool_id`
      -  :class:`~.tool.enums.ToolID`


Tool - Enums
------------------------------------

List of enums:

* :class:`~.tool.enums.ToolID`
* :class:`~.tool.enums.ToolCommand`

.. automodule:: pyniryo2.tool.enums
    :members:
    :undoc-members:
    :member-order: bysource