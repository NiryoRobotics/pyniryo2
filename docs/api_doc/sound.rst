Sound
=====================================

This file presents the different :ref:`functions <api_doc/sound:Sound - Command functions>`,
:ref:`enums <api_doc/sound:Sound - Enums>` and
:ref:`topics <api_doc/sound:Sound - Niryo Topics>` available with the Sound API

Sound - Command functions
------------------------------------

.. automodule:: pyniryo2.sound
   :members: Sound


This section reference all existing functions to control the Sound interface of the Ned2.
All functions are accessible via an instance of the class :ref:`NiryoRobot <api_doc/niryo_robot:NiryoRobot>` ::


    robot = NiryoRobot(<robot_ip_address>)

    robot.sound.play('connected.wav')
    ...


List of functions:

.. contents::
   :local:
   :depth: 1

.. autoclass:: Sound

Sound - Play
###########################

.. automethod:: Sound.play
.. automethod:: Sound.stop
.. autoproperty:: Sound.state
.. automethod:: Sound.say

Sound - Volume
###########################

.. autoproperty:: Sound.volume
.. automethod:: Sound.get_volume
.. automethod:: Sound.set_volume

Sound - Manage
###########################

.. autoproperty:: Sound.sounds
.. automethod:: Sound.get_sounds
.. automethod:: Sound.save
.. automethod:: Sound.delete
.. automethod:: Sound.get_sound_duration


Sound - Niryo Topics
------------------------------------

The use of these functions is explained in the :ref:`NiryoTopics <api_doc/niryo_topics:NiryoTopic>`, section.
They allow the acquisition of data in real time by callbacks or by direct call.

.. list-table:: Sound's Niryo Topics
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Function
      -  Return type
   *  -  ``/niryo_robot_sound/sound``
      -  :attr:`~.sound.Sound.state`
      -  :exc:`str`
   *  -  ``/niryo_robot_sound/sound_database``
      -  :attr:`~.sound.Sound.sounds`
      -  :exc:`dict`
   *  -  ``/niryo_robot_sound/volume``
      -  :attr:`~.sound.Sound.volume`
      -  :exc:`int`

Sound - Enums
------------------------------------

List of enums:

* :class:`~.sound.enums.ManageSound`
* :class:`~.sound.enums.Language`

.. automodule:: pyniryo2.sound.enums
    :members:
    :undoc-members:
    :member-order: bysource
