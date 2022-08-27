import asyncio
from typing import Optional

from msmart.device import air_conditioning
from msmart.scanner import MideaDiscovery
from msmart.const import OPEN_MIDEA_APP_ACCOUNT, OPEN_MIDEA_APP_PASSWORD

from homecontrol.aircon.structs import (
    ACConnectionError,
    ACConnectionInfo,
    ACInvalidState,
    ACState,
)


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
        self.device.power_state = state.power_state
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
        if state.eco_mode and state.turbo_mode:
            raise ACInvalidState(
                "Cannot have both eco_mode and turbo_mode true at the same time"
            )
        if not 16 <= state.target_temp <= 30:
            raise ACInvalidState("target_temp must be between 16 and 30")

    def get_state(self) -> ACState:
        """
        Refreshes the device and returns the current state

        :raises ACConnectionError: When there is a connection issue
        """
        # Attempt to refresh the device
        try:
            self.device.refresh()

            return self._get_state_from_device()
        except UnboundLocalError as exc:
            raise ACConnectionError(
                "An error occurred while attempting to refresh a unit's state"
            ) from exc

    def set_state(self, state: ACState) -> Optional[ACState]:
        """
        Attempts to assign the devices state

        :raises ACConnectionError: When there is a connection issue
        :raises ACInvalidState: When the given state is invalid
        """
        self._validate_state(state)
        self._assign_state_to_device(state)

        # Attempt to apply the state
        try:
            self.device.apply()

            return state
        except UnboundLocalError as exc:
            raise ACConnectionError(
                "An error occurred while attempting to apply a state to a unit"
            ) from exc

    @staticmethod
    def discover(name: str, ip_address: str) -> ACConnectionInfo:
        """
        Obtains connection information for air conditioning unit given its ip address

        :raises ACConnectionError: When there is a connection issue
        """
        found_devices = None
        try:
            discovery = MideaDiscovery(
                account=OPEN_MIDEA_APP_ACCOUNT,
                password=OPEN_MIDEA_APP_PASSWORD,
                amount=1,
            )
            loop = asyncio.new_event_loop()
            found_devices = loop.run_until_complete(discovery.get(ip_address))
            loop.close()
        except Exception as exc:
            raise ACConnectionError(
                "An error occurred while attempting to discover a device"
            ) from exc

        if found_devices:
            # Only looked for one anyway
            found_device = list(found_devices)[0]

            # Package the required info
            return ACConnectionInfo(
                name=name,
                ip_address=found_device.ip,
                port=found_device.port,
                identifier=found_device.id,
                key=found_device.key,
                token=found_device.token,
            )
        raise ACConnectionError(f"Unable to find the device with ip {ip_address}")
