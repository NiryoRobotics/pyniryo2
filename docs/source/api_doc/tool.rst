Tool
=====================================

This file presents the different :ref:`source/api_doc/tool:Tool - Command functions`,
:ref:`source/api_doc/tool:Tool - Enums` & :ref:`source/api_doc/tool:Tool - Niryo Topics` available with the Tool API


Tool - Command Functions
------------------------------------

.. automodule:: pyniryo2.tool.tool
   :members:
   :noindex:


This section reference all existing functions to control your robot, which include

- Using tools
- Using grippers
- Using the vacuum pump
- Using the electromagnet
- Management of the TCP

All functions to control the robot are accessible via an instance of
the class :ref:`source/api_doc/niryo_robot:NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.tool.update_tool()
    robot.tool.grasp_with_tool()
    robot.tool.release_with_tool()
    ...

See examples on :ref:`Examples Section <source/examples/examples_tool_action:Examples: Tool Action>`

List of functions subsections:

.. contents::
   :local:
   :depth: 1


Tool functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: Tool.update_tool
.. autoproperty:: Tool.tool
.. autoproperty:: Tool.get_current_tool_id
.. automethod:: Tool.grasp_with_tool
.. automethod:: Tool.release_with_tool

Grippers functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: Tool.open_gripper
.. automethod:: Tool.close_gripper

Vacuum pump functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: Tool.pull_air_vacuum_pump
.. automethod:: Tool.push_air_vacuum_pump

Electromagnet functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: Tool.setup_electromagnet
.. automethod:: Tool.activate_electromagnet
.. automethod:: Tool.deactivate_electromagnet

TCP functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automethod:: Tool.enable_tcp
.. automethod:: Tool.set_tcp
.. automethod:: Tool.reset_tcp

TCP functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: Tool
    :members: enable_tcp, set_tcp, reset_tcp
    :member-order: bysource

Tool - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`source/api_doc/niryo_topics:NiryoTopic` section.
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
    :noindex: