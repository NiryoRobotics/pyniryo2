# - Imports
from __future__ import print_function

# Python libraries
import roslibpy
import sys

# Communication imports
from pyniryo2.exceptions import RobotCommandException
from pyniryo2.robot_commander import RobotCommander

from pyniryo2.conveyor.enums import ConveyorID, ConveyorDirection, ConveyorStatus
from pyniryo2.conveyor.services import ConveyorServices
from pyniryo2.conveyor.topics import ConveyorTopics


class Conveyor(RobotCommander):
    # --- Public functions --- #
    def __init__(self, client):
        super(Conveyor, self).__init__(client)

        self._services = ConveyorServices(self._client)
        self._topics = ConveyorTopics(self._client)

    def set_conveyor(self):
        """
        Scan if a conveyor is plugged or not on a can bus. 
        If a new conveyor is detected, activate it and return its conveyor ID. 
        If a conveyor is already set, return its ID

        Example: ::
            # Get the id of the conveyor plugged
            conveyor_id = conveyor.set_conveyor()

            # Scan and set the conveyor plugged
            conveyor.set_conveyor()

        :return: New conveyor ID
        :rtype: int
        """
        cmd_type = ConveyorStatus.ADD.value
        req = self._services.get_ping_and_set_conveyor_request(cmd_type)
        resp = self._services.ping_and_set_conveyor_service.call(req)
        conveyor_id = resp["id"]

        # If new conveyor has been found
        if conveyor_id != ConveyorID.NONE.value:
            print("New conveyor detected and set with id :", conveyor_id)
            return conveyor_id
        else:
            last_conveyor_id = self.get_conveyors_feedback()[0].conveyor_id
            if last_conveyor_id != ConveyorID.NONE.value:
                print("No new conveyor detecter, actual conveyor id :", last_conveyor_id)
                return last_conveyor_id
            else:
                print("No conveyor detected")
                return last_conveyor_id

    def unset_conveyor(self, conveyor_id):
        """
        Remove and unset a conveyor previously plugged and set

        Example: ::
            conveyor_id = conveyor.set_conveyor()
            conveyor.unset_conveyor(conveyor_id)
        
        :param conveyor_id: Basically, ConveyorID.ID_1 or ConveyorID.ID_TWO
        :type conveyor_id: int
        :return: status, message
        :rtype: (int, str)
        """
        req = self._services.unset_conveyor_request(conveyor_id)
        resp = self._services.ping_and_set_conveyor_service.call(req)

        return str(resp["status"]), str(resp["message"])
    
    def run_conveyor(self, conveyor_id):
        """
        Run conveyor at id 'conveyor_id'

        Example: ::
            # Set the conveyor and get its id and un it. 
            # By default, the conveyor will go forward at a speed of 50
            # You can't choose the parameters with this method

            conveyor_id = conveyor.set_conveyor()
            conveyor.run_conveyor(conveyor_id) 

        :param conveyor_id: conveyor_id = conveyor_id
        :type conveyor_id: int
        :param control_on: True
        :type control_on: Bool
        :param speed: speed = 50
        :type speed: int
        :param direction: direction = ConveyorDirection.FORWARD.value
        :type direction: ConveyorDirection
        :rtype: None
        """
        req = self._services.control_conveyor_request(conveyor_id, control_on=True, speed=50, direction=ConveyorDirection.FORWARD.value)
        self._services.control_conveyor_service.call(req)

    def stop_conveyor(self, conveyor_id):
        """
        Run conveyor at id 'conveyor_id'
    
        Example: ::
            # Set the conveyor and get its id, run it and then stop it after 3 seconds
            # By default, the conveyor will go forward at a speed of 50
            # When the conveyor is stopped, its control_on parameter is False and its speed is 0

            import time

            conveyor_id = conveyor.set_conveyor()
            conveyor.run_conveyor(conveyor_id)
            time.sleep(3)
            conveyor.stop_conveyor(conveyor_id) 

        :param conveyor_id: conveyor_id = conveyor_id
        :type conveyor_id: int 
        :param control_on: False
        :type control_on: Bool
        :param speed: speed = 0
        :type speed: int
        :param direction: direction = ConveyorDirection.FORWARD.value
        :type direction: ConveyorDirection
        :rtype: None
        """
        req = self._services.control_conveyor_request(conveyor_id, control_on=False, speed=0, direction=ConveyorDirection.FORWARD.value)
        self._services.control_conveyor_service.call(req)

    def control_conveyor(self, conveyor_id, control_on, speed, direction):
        """
        Control conveyor associated to conveyor_id.
        Then stops it if bool_control_on is False, else refreshes it speed and direction

        Example: ::
            # Example 1
            # Set the conveyor and get its id, control it and then stop it after 3 seconds
            # It this first example, we control the conveyor at a speed of 100% and in the forward direction

            import time

            conveyor_id = conveyor.set_conveyor()
            conveyor.control_conveyo(conveyor_id, True, 100, ConveyorDirection.FORWARD.value)
            time.sleep(3)
            conveyor.stop_conveyor(conveyor_id) 

        # Example 2
            # Set the conveyor and get its id, control it and then stop it after 3 seconds
            # It this second example, we control the conveyor at a speed of 30% and in the backward direction

            import time

            conveyor_id = conveyor.set_conveyor()
            conveyor.control_conveyo(conveyor_id, True, 30, ConveyorDirection.BACKWARD.value)
            time.sleep(3)
            conveyor.stop_conveyor(conveyor_id) 

        :param conveyor_id: ConveyorID = conveyor_id
        :type conveyor_id: int
        :param bool_control_on: True for activate, False for deactivate
        :type bool_control_on: bool
        :param speed: target speed
        :type speed: int (0, 100)%
        :param direction: ConveyorDirection.FORWARD.value, ConveyorDirection.BACKWARD.value
        :type direction: ConveyorDirection
        :return: status, message
        :rtype: (int, str)
        """
        req = self._services.control_conveyor_request(conveyor_id, control_on, speed, direction)
        resp = self._services.control_conveyor_service.call(req)

        return str(resp["status"]), str(resp["message"])
        
    @property
    def get_conveyors_feedback(self):
        """
        Give conveyors feedback (conveyor_id, connection_state, running, speed, direction)

        :return: namedtuple[conveyor_id, connection_state, running, speed, direction]
        :rtype: namedtuple(int, bool, bool, int, int)
        """
        return self._topics.conveyor_feedback_topic
