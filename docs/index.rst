PyNiryo2 Documentation
================================

.. image:: _static/PyNiryo_logo_2.png
   :width: 600px
   :align: center


This documentation presents Ned's PyPi package, which is the second version of the python API Pyniryo for the robots:
Niryo One, Ned and Ned2. It is based on the roslibpy library and allows a more complete programming of the robots.

It offers a simple way for developers to create programs for robot and
to control them via remote communication from their computers.
Contrary to the Python ROS Wrapper, the user will not need to be connected on the robot
through a terminal.
This API is based on `roslibpy <https://roslibpy.readthedocs.io/en/latest/index.html>`_.

.. note:: This package is able to control Ned in simulation
   as well as the physical robot.

.. figure:: images/niryo_ned_front.jpg
   :alt: Niryo Ned
   :height: 400px
   :align: center

   Niryo Ned

.. list-table::
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  - Functionality
      - PyNiryo
      - PyNiryo2
   *  - Robot control
      - **YES**
      - **YES**
   *  - Callbacks functions
      - **NO**
      - **YES**
   *  - Parallelism of commands
      - **NO**
      - **YES**
   *  - Asynchronous functions
      - **NO**
      - **YES**


Before getting started
----------------------------


| If you haven’t already done so , make sure to learn about
 the ROS robot software by reading the |ros_doc|_.

| This documentation also contains everything you need to
 know if you want to use Ned through simulation.


Sections organization
-----------------------------------

This document is organized in 4 main sections

Setup
^^^^^^^^^^^

Install & Setup your environment in order to use Ned with PyNiryo2.

Firstly, follow :doc:`Installation instructions <source/setup/installation>`,
then :doc:`find your Robot IP address <source/setup/ip_address>` to be ready.

.. toctree::
   :caption: Setup
   :hidden:

   source/setup/installation
   source/setup/ip_address
   source/setup/verify_setup

Examples
^^^^^^^^^^^^^^^

Learn how to use the PyNiryo2 package to implement various tasks

.. toctree::
   :hidden:
   :caption: Examples

   source/examples/examples_basics
   source/examples/examples_movement
   source/examples/examples_tool_action
   source/examples/examples_conveyor
   source/examples/examples_vision
   source/examples/examples_frames
   source/examples/code_templates

API Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Master controls with PyNiryo2 with full detailed functions
:doc:`here <source/api_doc/niryo_robot>`

.. toctree::
   :caption: API Documentation

   source/api_doc/niryo_robot
   source/api_doc/niryo_topics
   source/api_doc/niryo_ros
   source/api_doc/arm
   source/api_doc/tool
   source/api_doc/vision
   source/api_doc/io
   source/api_doc/conveyor
   source/api_doc/saved_poses
   source/api_doc/pick_place
   source/api_doc/trajectories
   source/api_doc/frames
   source/api_doc/led_ring
   source/api_doc/sound




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |ros_doc| replace:: Ned's Software documentation
.. _ros_doc: https://docs.niryo.com/ros-doc/
