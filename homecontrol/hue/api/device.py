from typing import List
from homecontrol.helpers import ResponseStatus, dicts_to_list, object_to_dict
from homecontrol.hue.api.structs import DeviceGet, RoomGet, RoomPut
from homecontrol.hue.exceptions import HueAPIError
from homecontrol.hue.session import HueBridgeSession


class Device:
    """
    Handles Philips Hue Device endpoints
    """

    _session: HueBridgeSession

    def __init__(self, session: HueBridgeSession) -> None:
        self._session = session

    def get_devices(self) -> List[DeviceGet]:
        """
        Returns a list of devices
        """

        return self._session.get_resource(
            endpoint="/clip/v2/resource/device",
            class_type=DeviceGet,
            error_message="An error occurred trying to get devices.",
        )

    def get_device(self, identifier: str) -> DeviceGet:
        """
        Returns information about a device
        """
        return self._session.get_resource(
            endpoint=f"/clip/v2/resource/device/{identifier}",
            class_type=DeviceGet,
            error_message=f"An error occurred trying to get data about the device with id {identifier}.",
        )[0]
