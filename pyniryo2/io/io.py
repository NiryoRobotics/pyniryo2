# Communication imports
from pyniryo2.robot_commander import RobotCommander
from pyniryo2.enums import RobotErrors
from pyniryo2.exceptions import RobotCommandException

from pyniryo2.io.services import IOServices
from pyniryo2.io.topics import IOTopics
from pyniryo2.io.enums import PinID, PinMode, PinState


class IO(RobotCommander):
    # --- Public functions --- #
    def __init__(self, client):
        super(IO, self).__init__(client)

        self._services = IOServices(self._client)
        self._topics = IOTopics(self._client)

    @property
    def get_io_state(self):
        """
        Returns the io state client which can be used synchronously or asynchronously to obtain the io states.
        The io state client returns a list of DigitalPinObject.

        Examples: ::

            # Get last value
            io.get_io_state()
            io.get_io_state.value

            # Subscribe a callback
            def io_callback(io_state):
                print io_state

            arm.get_io_state.subscribe(io_callback)
            arm.get_io_state.unsubscribe()

        :return: io state topic instance
        :rtype: NiryoTopic
        """
        return self._topics.joint_states_topic

    def set_pin_mode(self, pin_id, pin_mode):
        """
        Set pin number pin_id to mode pin_mode

        Examples: ::
            io.set_pin_mode(PinID.GPIO_1A, PinMode.INPUT)
            io.set_pin_mode(PinID.GPIO_1A, PinMode.OUTPUT)

        :param pin_id:
        :type pin_id: PinID
        :param pin_mode:
        :type pin_mode: PinMode
        :return: True if command where successfully completed, False otherwise.
        :rtype: Bool
        """
        self._check_enum_belonging(pin_id, PinID)
        self._check_enum_belonging(pin_mode, PinMode)

        req = self._services.set_digital_io_mode_request(pin_id, pin_mode)
        resp = self._services.set_digital_io_mode_service.call(req)
        return resp["status"] >= RobotErrors.SUCCESS.value

    def digital_write(self, pin_id, digital_state):
        """
        Set pin_id state to digital_state

        Examples: ::
            io.digital_write(PinID.GPIO_1A, PinState.HIGH)
            io.digital_write(PinID.GPIO_1A, PinState.LOW)

        :param pin_id:
        :type pin_id: PinID
        :param digital_state:
        :type digital_state: PinState
        :return: True if command where successfully completed, False otherwise.
        :rtype: Bool
        """
        self._check_enum_belonging(pin_id, PinID)
        self._check_enum_belonging(digital_state, PinState)

        req = self._services.set_digital_io_state_request(pin_id, digital_state)
        resp = self._services.set_digital_io_state_service.call(req)

        if resp["status"] == RobotErrors.DIGITAL_IO_PANEL_ERROR.value:
            raise RobotCommandException("Error {}: {}".format(resp["status"], resp["message"]))

        return resp["status"] >= RobotErrors.SUCCESS.value

    def digital_read(self, pin_id):
        """
        Read pin number pin_id and return its state

        Examples: ::
           io.set_pin_mode(PinID.GPIO_1A, PinMode.OUTPUT)
           io.digital_read(PinID.GPIO_1A) #type = PinState
           io.digital_read(PinID.GPIO_1A).value #type = int
           bool(io.digital_read(PinID.GPIO_1A).value) #type = bool

        :param pin_id:
        :type pin_id: PinID
        :rtype: PinState
        """
        self._check_enum_belonging(pin_id, PinID)

        req = self._services.get_digital_io_request(pin_id)
        resp = self._services.get_digital_io_service.call(req)

        if resp["status"] < RobotErrors.SUCCESS.value:
            return None

        return self._services.get_digital_io_response_to_object(resp)
