Tool
=====================================

Tool - Command Functions
------------------------------------

.. automodule:: pyniryo2.tool.tool
   :members:


This section reference all existing functions to control your robot, which include

- Using tools
- Using grippers
- Using the vacuum pump
- Using the electromagnet

All functions to control the robot are accessible via an instance of
the class :class:`~.api.enums_communication.NiryoRobot` ::


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


Tool Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: update_tool, tool, get_current_tool_id, grasp_with_tool, release_with_tool
    :member-order: bysource

Grippers Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: open_gripper, close_gripper
    :member-order: bysource

Vacuum Pump Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: pull_air_vacuum_pump, push_air_vacuum_pump
    :member-order: bysource

Electromagnet Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: setup_electromagnet, activate_electromagnet, deactivate_electromagnet
    :member-order: bysource


Tool - Enums
------------------------------------

List of enums:

* :class:`~.tool.objects.ToolID`
* :class:`~.tool.objects.ToolCommand`

.. automodule:: tool.enums
    :members:
    :undoc-members:
    :member-order: bysource

.. automodule:: io.enums
    :members:
    :undoc-members:
    :exclude-members: PinState, PinMode
    :member-order: bysource