import asyncio
from typing import Optional

from msmart.device import air_conditioning
from msmart.scanner import MideaDiscovery

from homecontrol.aircon.exceptions import ACInvalidStateError
from homecontrol.aircon.structs import ACAccountConfig, ACConnectionInfo, ACState
from homecontrol.exceptions import DeviceConnectionError


class ACDevice:
    """
    Wrapper for msmart's air_conditioning object
    """

    device: air_conditioning
    connection_info: ACConnectionInfo

    def __init__(self, connection_info: ACConnectionInfo) -> None:
        """
        Creates the msmart device instance and authenticates it
        """
        self.connection_info = connection_info
        self.device = air_conditioning(
            self.connection_info.ip_address,
            self.connection_info.identifier,
            self.connection_info.port,
        )
        self.device.authenticate(self.connection_info.key, self.connection_info.token)
        self.device.get_capabilities()

    def _get_state_from_device(self) -> ACState:
        """
        Returns the current state from the device (but does not refresh it first)
        """
        return ACState(
            power=self.device.power_state,
            prompt_tone=self.device.prompt_tone,
            target=self.device.target_temperature,
            mode=self.device.operational_mode,
            fan=self.device.fan_speed,
            swing=self.device.swing_mode,
            eco=self.device.eco_mode,
            turbo=self.device.turbo_mode,
            fahrenheit=self.device.fahrenheit,
            indoor=self.device.indoor_temperature,
            outdoor=self.device.outdoor_temperature,
        )

    def _assign_state_to_device(self, state: ACState):
        """
        Assigns the state of the device (but does not update it)
        """
        self.device.power_state = state.power
        self.device.prompt_tone = state.prompt_tone
        self.device.target_temperature = state.target
        self.device.operational_mode = state.mode
        self.device.fan_speed = state.fan
        self.device.swing_mode = state.swing
        self.device.eco_mode = state.eco
        self.device.turbo_mode = state.turbo
        self.device.fahrenheit = state.fahrenheit

    def _validate_state(self, state: ACState):
        """
        Validates a state (for use before it is sent to a device)

        TODO: Take account of fahrenheit
        """
        if state.eco and state.turbo:
            raise ACInvalidStateError(
                "Cannot have both eco and turbo true at the same time"
            )
        if not 16 <= state.target <= 30:
            raise ACInvalidStateError("target_temp must be between 16 and 30")

    def get_state(self) -> ACState:
        """
        Refreshes the device and returns the current state

        Raises:
            DeviceConnectionError: When there is a connection issue
        """
        # Attempt to refresh the device
        try:
            self.device.refresh()

            return self._get_state_from_device()
        except UnboundLocalError as err:
            raise DeviceConnectionError(
                "An error occurred while attempting to refresh an AC unit's state"
            ) from err

    def set_state(self, state: ACState) -> Optional[ACState]:
        """
        Attempts to assign the devices state

        Raises:
            DeviceConnectionError: When there is a connection issue
            ACInvalidState: When the given state is invalid
        """
        self._validate_state(state)
        self._assign_state_to_device(state)

        # Attempt to apply the state
        try:
            self.device.apply()

            return state
        except UnboundLocalError as err:
            raise DeviceConnectionError(
                "An error occurred while attempting to apply a state to a AC unit"
            ) from err

    @staticmethod
    def discover(
        name: str, ip_address: str, account_config: ACAccountConfig
    ) -> ACConnectionInfo:
        """
        Obtains connection information for air conditioning unit given its ip address

        Raises:
            DeviceConnectionError: When there is a connection issue
        """
        found_devices = None
        try:
            discovery = MideaDiscovery(
                account=account_config.username,
                password=account_config.password,
                amount=1,
            )
            loop = asyncio.new_event_loop()
            found_devices = loop.run_until_complete(discovery.get(ip_address))
            loop.close()
        except Exception as err:
            raise DeviceConnectionError(
                "An error occurred while attempting to discover an AC unit"
            ) from err

        if found_devices:
            # Only looked for one anyway
            found_device = list(found_devices)[0]

            # Validate auth data was obtained correctly
            if found_device.key is None or found_device.token is None:
                raise DeviceConnectionError("Unable to obtain authentication info")

            # Package the required info
            return ACConnectionInfo(
                name=name,
                ip_address=found_device.ip,
                port=found_device.port,
                identifier=found_device.id,
                key=found_device.key,
                token=found_device.token,
            )
        raise DeviceConnectionError(f"Unable to find the AC unit with ip {ip_address}")
