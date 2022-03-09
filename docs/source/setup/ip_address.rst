Find your Robot's IP address
=================================

In order to use your robot through TCP connection, you will firstly need
to connect to it, which imply that you know its IP Address

The next sections explain how to find your robot IP according to your configuration:

.. contents::
   :local:
   :depth: 1

Hotspot mode
----------------------------------------
If you are directly connected to your robot through its wifi, the IP Address
you will need to use is ``10.10.10.10``

Simulation or directly on the robot
----------------------------------------
In this situation, the Robot is running on the same computer as the client,
the IP Address will be the localhost address ``127.0.0.1``


Direct Ethernet connection
----------------------------------------
If you are directly connected to your robot with an ethernet cable, the static IP of your
robot will be ``169.254.200.200``

The reader should note that he may has to change his wired settings to allow the connection.
See how |link_ethernet|_

Computer and Robot Connected on the same router
-------------------------------------------------------------

You will need to find the robot address using ``nmap``, or you can also use search button
of Niryo Studio to see which robots are available

You can also make IP permanent so that you won't have to search for it next time

.. |link_ethernet| replace:: Connect to Ned via Ethernet on Ubuntu
.. _link_ethernet: https://niryo.com/docs/niryo-one/developer-tutorials/connect-to-niryo-one-via-ethernet-on-ubuntu/
