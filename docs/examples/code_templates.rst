Code templates
==============

As code structures are always the same, we wrote down few templates for you
to start your code file with a good form

The short template
-------------------

Very simple, straightforward ::

    from pyniryo2 import *

    # Connect to robot & calibrate
    robot = NiryoRobot(<robot_ip_address>)
    robot.arm.calibrate_auto()

    # --- --------- --- #
    # --- YOUR CODE --- #
    # --- --------- --- #

.. toggle::

    .. image:: ../../images/code_template_basic.*
       :align: center

Advanced template
-------------------

This template let the user defined his own process but it handles connection,
calibration, tool equipping, and make the robot go to sleep at the end ::

    from pyniryo2 import *

    local_mode = False # Or True
    tool_used = ToolID.GRIPPER_1
    # Set robot address
    robot_ip_address_rpi = "x.x.x.x"
    robot_ip_address_local = "127.0.0.1"

    robot_ip_address = robot_ip_address_local if local_mode else robot_ip_address_rpi


    def process(niryo_edu):
        # --- --------- --- #
        # --- YOUR CODE --- #
        # --- --------- --- #

    if __name__ == '__main__':
        # Connect to robot
        robot = NiryoRobot(robot_ip_address)
        # Calibrate robot if robot needs calibration
        robot.arm.calibrate_auto()
        # Equip tool
        robot.tool.update_tool()
        # Launching main process
        process(client)
        # Ending
        robot.arm.go_to_sleep()

Advanced template for conveyor
--------------------------------------

Same as :ref:`examples/code_templates:Advanced template` but with a conveyor ::

    from pyniryo2 import *

    # Set robot address
    robot_ip_address = "x.x.x.x"


    def process(robot, conveyor_id):
        robot.conveyor.run_conveyor(conveyor_id)

        # --- --------- --- #
        # --- YOUR CODE --- #
        # --- --------- --- #

        robot.conveyor.stop_conveyor()


    if __name__ == '__main__':
        # Connect to robot
        robot = NiryoRobot(robot_ip_address)
        # Calibrate robot if robot needs calibration
        robot.arm.calibrate_auto()
        # Equip tool
        robot.tool.update_tool()
        # Activating connexion with conveyor
        conveyor_id = robot.conveyor.set_conveyor()
        # Launching main process
        process(robot, conveyor_id)
        # Ending
        robot.arm.go_to_sleep()
        # Deactivating connexion with conveyor
        robot.conveyor.unset_conveyor(conveyor_id)


Advanced template for vision
--------------------------------------

Huge template for vision users ! ::

    from pyniryo2 import *

    local_mode = False # Or True
    workspace_name = "workspace_1"  # Robot's Workspace Name
    # Set robot address
    robot_ip_address_rpi = "x.x.x.x"
    robot_ip_address_local = "127.0.0.1"

    robot_ip_address = robot_ip_address_local if local_mode else robot_ip_address_rpi

    # The pose from where the image processing happens
    observation_pose = PoseObject(
        x=0.18, y=0.0, z=0.35,
        roll=0.0, pitch=1.57, yaw=-0.2,
    )

    # Center of the conditioning area
    place_pose = PoseObject(
        x=0.0, y=-0.23, z=0.12,
        roll=0.0, pitch=1.57, yaw=-1.57
    )

    def process(robot):
        robot.arm.move_pose(observation_pose)
        catch_count = 0
        while catch_count < 3:
            ret = robot.vision.get_target_pose_from_cam(workspace_name,
                                                        height_offset=0.0,
                                                        shape=ObjectShape.ANY,
                                                        color=ObjectColor.ANY)
            obj_found, obj_pose, shape, color = ret
            if not obj_found:
                continue
            catch_count += 1
            # --- --------- --- #
            # --- YOUR CODE --- #
            # --- --------- --- #
            robot.pick_place.place_from_pose(place_pose)

    if __name__ == '__main__':
        # Connect to robot
        robot = NiryoRobot(robot_ip_address)
        # Calibrate robot if robot needs calibration
        robot.arm.calibrate_auto()
        # Equip tool
        robot.tool.update_tool()
        # Launching main process
        process(client)
        # Ending
        robot.arm.go_to_sleep()


Callbacks Templates 
--------------------------------------

Template for event integration ! ::

    # Imports
    from pyniryo2 import *
    from threading import Event

    robot_ip = "xxx.xxx.xxx.xxx"
    robot_ip_address_local = "127.0.0.1"

    # Events
    update_tool_event = Event()
    update_tool_event.clear()

    calibrated_event = Event()
    calibrated_event.clear()

    # Poses
    pose_1 = PoseObject()

    pose_2 = PoseObject()

    # Callbacks
    def update_tool_success_callback(result):
        update_tool_event.set()
        print 'Update Tool: ', result['message']

    def update_tool_error_callback(result):
        print 'Update Tool: ', result['message']

    def calibrate_success_callback(result):
        calibrated_event.set()
        print 'Calibrate Callback: ', result["message"]

    def calibrate_error_callback(result):
        print 'Calibrate Callback: ', result["message"]

        """
        Add Callbacks Here
        """

    def action_function(robot):

        """
        Don't put niryo_robot in parameter, it will take the pyniryo2 package
        add your function here
        """


    if __name__ == "__main__":

        # Connect to robot
        robot = NiryoRobot(robot_ip)

        # Calibrate robot if robot needs calibration
        robot.arm.calibrate_auto(callback=calibrate_success_callback, errback=calibrate_error_callback)
        calibrated_event.wait(20)
        if not calibrated_event.is_set():
            quit

        robot.tool.update_tool(callback=update_tool_success_callback, errback=update_tool_error_callback)
        update_tool_event.wait()

        action_function(robot)

        robot.arm.go_to_sleep()

