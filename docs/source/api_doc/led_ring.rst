Led Ring
=====================================

This file presents the different :ref:`functions <source/api_doc/led_ring:Led Ring - Command functions>`,
:ref:`enums <source/api_doc/led_ring:Led Ring - Enums>`,
:ref:`topics <source/api_doc/led_ring:Led Ring - Niryo Topics>` and
:ref:`objects <source/api_doc/led_ring:Led Ring - Objects>` available with the Led Ring API

Led Ring - Command functions
------------------------------------

.. automodule:: pyniryo2.led_ring
   :members: LedRing


This section reference all existing functions to control the Led Ring, which are several parameterizable animations.
All functions are accessible via an instance of the class :ref:`NiryoRobot <source/api_doc/niryo_robot:NiryoRobot>` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.led_ring.solid([255, 255, 255])
    ...


List of functions:

.. contents::
   :local:
   :depth: 1

* :class:`LedRing`

.. autoproperty:: LedRing.status
.. automethod:: LedRing.get_status
.. automethod:: LedRing.solid
.. automethod:: LedRing.turn_off
.. automethod:: LedRing.flash
.. automethod:: LedRing.alternate
.. automethod:: LedRing.chase
.. automethod:: LedRing.wipe
.. automethod:: LedRing.snake
.. automethod:: LedRing.breath
.. automethod:: LedRing.rainbow
.. automethod:: LedRing.rainbow_cycle
.. automethod:: LedRing.rainbow_chase
.. automethod:: LedRing.go_up
.. automethod:: LedRing.go_up_down
.. automethod:: LedRing.custom
.. automethod:: LedRing.set_led_color

Led Ring - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`NiryoTopics <source/api_doc/niryo_topics:NiryoTopic>`, section.
They allow the acquisition of data in real time by callbacks or by direct call.

.. list-table:: Led Ring's Niryo Topics
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Function
      -  Return type
   *  -  ``/status``
      -  :attr:`~.led_ring.LedRing.status`
      -  :class:`~.led_ring.objects.LedRingStatusObject`



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