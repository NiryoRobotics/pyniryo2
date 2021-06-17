# - Imports
from __future__ import print_function

# Communication imports
from pyniryo2.robot_commander import RobotCommander
from pyniryo2.enums import RobotErrors
from pyniryo2.io.enums import PinID

from pyniryo2.tool.enums import ToolID, ToolCommand
from pyniryo2.tool.services import ToolServices
from pyniryo2.tool.actions import ToolActions
from pyniryo2.tool.topics import ToolTopics


class Tool(RobotCommander):
    def __init__(self, client):
        super(Tool, self).__init__(client)

        self._services = ToolServices(self._client)
        self._topics = ToolTopics(self._client)
        self._actions = ToolActions(self._client)

        self.__action_timeout = 10

    @property
    def tool(self):
        return self.get_current_tool_id()

    @property
    def get_current_tool_id(self):
        """
        Returns the equipped tool Id client which can be used synchronously or asynchronously
        to obtain the equipped tool Id.
        The topic returns a attribute of the ToolID enum.

        Examples: ::

            # Get last value
            tool.get_current_tool_id()
            tool.get_current_tool_id.value

            # Subscribe a callback
            def tool_id_callback(tool_id_object):
                print tool_id_object

            tool.get_current_tool_id.subscribe(tool_id_callback)
            tool.get_current_tool_id.unsubscribe()

        :return: the equipped tool Id topic instance.
        :rtype: NiryoTopic
        """
        return self._topics.tool_id_topic

    def update_tool(self, callback=None, errback=None, timeout=None):
        """
        Update equipped tool

        Examples: ::
            # Synchronous use
            tool.update_tool()

            # Asynchronous use
            def update_tool_callback(result):
                if result["status"] < RobotErrors.SUCCESS.value:
                    print("Update failed")
                else:
                    print("Update completed with success")

            tool.update_tool(update_tool_callback)

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :param errback: Callback invoked on error.
        :type errback: function
        :param timeout: Timeout for the operation, in seconds. Only used if blocking.
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        req = self._services.get_trigger_request()
        result = self._services.update_tool_service.call(req, callback, errback, timeout)
        return True if callback is None or result["status"] >= RobotErrors.SUCCESS.value else False

    def grasp_with_tool(self, callback=None):
        """
        Grasp with tool
        | This action correspond to
        | - Close gripper for Grippers
        | - Pull Air for Vacuum pump
        | - Activate for Electromagnet
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::
            tool.update_tool()
            tool.grasp_with_tool()
            
            def tool_callback(_msg)
                print("Grasped") 
                
            tool.grasp_with_tool(callback=tool_callback)

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        tool_id = self.get_current_tool_id()

        if tool_id in (ToolID.GRIPPER_1, ToolID.GRIPPER_2, ToolID.GRIPPER_3, ToolID.GRIPPER_4):
            return self.close_gripper(callback=callback)
        elif tool_id == ToolID.VACUUM_PUMP_1:
            return self.pull_air_vacuum_pump(callback=callback)
        elif tool_id == ToolID.ELECTROMAGNET_1:
            return self.activate_electromagnet(callback=callback)

    def release_with_tool(self, callback=None):
        """
        Release with tool
        | This action correspond to
        | - Open gripper for Grippers
        | - Push Air for Vacuum pump
        | - Deactivate for Electromagnet
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::
            tool.update_tool()
            tool.release_with_tool()
            
            def tool_callback(_msg)
                print("Released")
                
            tool.release_with_tool(callback=tool_callback)

        :param callback: Callback invoked on successful execution.
        :type callback: function
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        tool_id = self.get_current_tool_id()

        if tool_id in (ToolID.GRIPPER_1, ToolID.GRIPPER_2, ToolID.GRIPPER_3, ToolID.GRIPPER_4):
            return self.open_gripper(callback=callback)
        elif tool_id == ToolID.VACUUM_PUMP_1:
            return self.push_air_vacuum_pump(callback=callback)
        elif tool_id == ToolID.ELECTROMAGNET_1:
            return self.deactivate_electromagnet(callback=callback)

    # - Gripper
    def open_gripper(self, speed=500, callback=None):
        """
        Open gripper associated to the equipped gripper with a speed 'speed'
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::
            tool.update_tool()
            tool.open_gripper()
            tool.open_gripper(speed=850)
            
            def tool_callback(_msg)
                print("Released")
                
            tool.open_gripper(callback=tool_callback)

        :param speed: Between 100 & 1000
        :type speed: int
        :param callback: Callback invoked on successful execution.
        :type callback: function
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        speed = self._transform_to_type(speed, int)
        tool_id = self.get_current_tool_id()

        goal = self._actions.get_gripper_action_goal(tool_id, ToolCommand.OPEN_GRIPPER, speed)
        goal.send(result_callback=callback)

        if callback is None:
            return True

        result = goal.wait(self.__action_timeout)
        return True if result["status"] >= RobotErrors.SUCCESS.value else False

    def close_gripper(self, speed=500, callback=None):
        """
        Close gripper associated to 'gripper_id' with a speed 'speed'
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::
            tool.update_tool()
            tool.close_gripper()
            tool.close_gripper(speed=850)

            def tool_callback(_msg)
                print("Grasped")

            tool.close_gripper(callback=tool_callback)

        :param speed: Between 100 & 1000
        :type speed: int
        :param callback: Callback invoked on successful execution.
        :type callback: function
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        speed = self._transform_to_type(speed, int)
        tool_id = self.get_current_tool_id()

        goal = self._actions.get_gripper_action_goal(tool_id, ToolCommand.CLOSE_GRIPPER, speed)
        goal.send(result_callback=callback)

        if callback is None:
            return True

        result = goal.wait(self.__action_timeout)
        return True if result["status"] >= RobotErrors.SUCCESS.value else False

    # - Vacuum
    def pull_air_vacuum_pump(self, callback=None):
        """
        Pull air of vacuum pump
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::
            tool.update_tool()
            tool.pull_air_vacuum_pump()

            def tool_callback(_msg)
                print("Grasped")

            tool.pull_air_vacuum_pump(callback=tool_callback)


        :param callback: Callback invoked on successful execution.
        :type callback: function
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        goal = self._actions.get_vacuum_pump_action_goal(ToolCommand.PULL_AIR_VACUUM_PUMP)
        goal.send(result_callback=callback)
        
        if callback is None:
            return True

        result = goal.wait(self.__action_timeout)
        return True if result["status"] >= RobotErrors.SUCCESS.value else False

    def push_air_vacuum_pump(self, callback=None):
        """
        Push air of vacuum pump
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::
            tool.update_tool()
            tool.push_air_vacuum_pump()

            def tool_callback(_msg)
                print("Released")

            tool.push_air_vacuum_pump(callback=tool_callback)


        :param callback: Callback invoked on successful execution.
        :type callback: function
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        goal = self._actions.get_vacuum_pump_action_goal(ToolCommand.PUSH_AIR_VACUUM_PUMP)
        goal.send(result_callback=callback)
        
        if callback is None:
            return True

        result = goal.wait(self.__action_timeout)
        return True if result["status"] >= RobotErrors.SUCCESS.value else False

    # - Electromagnet
    def setup_electromagnet(self, pin_id):
        """
        Setup electromagnet on pin

        Example: ::
            tool.setup_electromagnet(PinID.GPIO_1A)
        
        :param pin_id:
        :type pin_id: PinID
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        self._check_enum_belonging(pin_id, PinID)

        req = self._services.equip_electromagnet_service_request()
        self._services.equip_electromagnet_service(req)

        goal = self._actions.get_electromagnet_action_goal(ToolCommand.SETUP_DIGITAL_IO, pin_id)
        goal.send()
        result = goal.wait(self.__action_timeout)

        return True if result["status"] >= RobotErrors.SUCCESS.value else False

    def activate_electromagnet(self, pin_id=-1, callback=None):
        """
        Activate electromagnet associated to electromagnet_id on pin_id
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::
            tool.setup_electromagnet(PinID.GPIO_1A)
            tool.activate_electromagnet()
            tool.activate_electromagnet(PinID.GPIO_1A)
            
            def tool_callback(_msg)
                print("Grasped") 
                
            tool.activate_electromagnet(callback=tool_callback)
            
        :param pin_id:
        :type pin_id: PinID
        :param callback: Callback invoked on successful execution.
        :type callback: function
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        self._check_enum_belonging(pin_id, PinID)

        req = self._services.equip_electromagnet_service_request()
        self._services.equip_electromagnet_service(req)

        goal = self._actions.get_electromagnet_action_goal(ToolCommand.ACTIVATE_DIGITAL_IO, pin_id)
        goal.send(result_callback=callback)

        if callback is None:
            return True

        result = goal.wait(self.__action_timeout)
        return True if result["status"] >= RobotErrors.SUCCESS.value else False

    def deactivate_electromagnet(self, pin_id=-1, callback=None):
        """
        Deactivate electromagnet associated to electromagnet_id on pin_id
        If a callback function is not passed in parameter, the function will be blocking.
        Otherwise, the callback will be called when the execution of the function is finished.

        Examples: ::
            tool.setup_electromagnet(PinID.GPIO_1A)
            tool.deactivate_electromagnet()
            tool.deactivate_electromagnet(PinID.GPIO_1A)

            def tool_callback(_msg)
                print("Deactivated")

            tool.deactivate_electromagnet(callback=tool_callback)
            
        :param pin_id:
        :type pin_id: PinID
        :param callback: Callback invoked on successful execution.
        :type callback: function
        :return: True if command where successfully completed, False otherwise.
        Returns always True with non blocking use.
        :rtype: Bool
        """
        self._check_enum_belonging(pin_id, PinID)

        req = self._services.equip_electromagnet_service_request()
        self._services.equip_electromagnet_service(req)

        goal = self._actions.get_electromagnet_action_goal(ToolCommand.DEACTIVATE_DIGITAL_IO, pin_id)
        goal.send(result_callback=callback)

        if callback is None:
            return True

        result = goal.wait(self.__action_timeout)
        return True if result["status"] >= RobotErrors.SUCCESS.value else False
