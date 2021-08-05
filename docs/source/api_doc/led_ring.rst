Led Ring
=====================================

This file presents the different :ref:`Led Ring - Command functions`,
:ref:`Led Ring - Enums`, :ref:`Led Ring - Niryo Topics` & :ref:`Led Ring - Objects` available with the Led Ring API

Led Ring - Command functions
------------------------------------

.. automodule:: pyniryo2.led_ring.led_ring
   :members: LedRing


This section reference all existing functions to control the Led Ring, which are several parameterizable animations.
All functions are accessible via an instance of the class :ref:`NiryoRobot` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.led_ring.led_ring_solid([255, 255, 255])
    ...


List of functions:

.. contents::
   :local:
   :depth: 1

.. autoclass:: LedRing
    :members: led_ring_solid, led_ring_turn_off, led_ring_flash, led_ring_alternate, 
                led_ring_chase, led_ring_wipe, led_ring_rainbow, led_ring_rainbow_cycle,
                led_ring_rainbow_chase, led_ring_go_up, led_ring_go_up_down
    :member-order: bysource



Led Ring - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`NiryoTopic` section.
They allow the acquisition of data in real time by callbacks or by direct call.

.. list-table:: Led Ring's Niryo Topics
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Function
      -  Return type
   *  -  ``/led_ring_status``
      -  :attr:`~.led_ring.LedRing.led_ring_status`
      -  :class:`~.led_ring.objects.LedRingStatusObject`
   *  -  ``led_ring_current_state``
      -  :attr:`~.led_ring.LedRing.led_ring_colors`
      -  :class:`~.led_ring.LedRingStateObject`


Led Ring - Enums
------------------------------------

List of enums:

* :class:`~.led_ring.enums.AnimationMode`
* :class:`~.led_ring.enums.LedMode`

.. automodule:: pyniryo2.led_ring.enums
    :members:
    :undoc-members:
    :member-order: bysource


Led Ring - Objects
------------------------------------

.. automodule:: pyniryo2.led_ring.objects
    :members:
    :no-undoc-members:
    :member-order: bysource