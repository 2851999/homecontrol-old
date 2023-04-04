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
        Returns a list of rooms
        """
        response = self._session.get("/clip/v2/resource/device")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get devices. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        # Obtain the data
        data = response.json()["data"]
        return dicts_to_list(DeviceGet, data)

    def get_device(self, identifier: str) -> DeviceGet:
        """
        Returns information about a device
        """
        response = self._session.get(f"/clip/v2/resource/device/{identifier}")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get data about the device with id {identifier}. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        # Obtain the data
        data = response.json()["data"]
        return dicts_to_list(DeviceGet, data)[0]
