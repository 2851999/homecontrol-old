from typing import List, Optional

from homecontrol.aircon.structs import ACState
from homecontrol.client.exceptions import APIError
from homecontrol.client.session import APISession
from homecontrol.helpers import ResponseStatus, dataclass_from_dict


class Aircon:
    """
    Handles aircon endpoints
    """

    _session: APISession

    def __init__(self, session: APISession) -> None:
        self._session = session

    def list_devices(self) -> List[str]:
        """
        Returns a list of registered device names
        """
        response = self._session.get("/ac/devices")
        if response.status_code != ResponseStatus.OK:
            raise APIError("An error occured listing devices")
        return response.json()

    def register_device(
        self, name: str, ip_address: str, retries: Optional[int] = None
    ) -> bool:
        """
        Registers a device with the API

        :param name: Name of the device to register
        :param ip_address: IP address of the device to register
        :param retries: Number of times to try
        :return: Whether registration was successful or not
        """
        attempts = 1 if retries is None else retries
        current_attempt = 0
        while current_attempt < attempts:
            response = self._session.put(
                "/ac/devices/register", json={"name": name, "ip": ip_address}
            )

            if response.status_code == ResponseStatus.CREATED:
                return True
            current_attempt += 1
        return False

    def get_device(self, name: str) -> ACState:
        """
        Returns the state of a device
        """
        response = self._session.get(f"/ac/devices/{name}")
        if response.status_code != ResponseStatus.OK:
            raise APIError(f"An error occured getting the state of {name}")
        return dataclass_from_dict(ACState, response.json())

    def set_device(self, name: str, state: ACState) -> ACState:
        """
        Sets the state of a device
        """
        response = self._session.put(f"/ac/devices/{name}", json=state.__dict__)
        if response.status_code != ResponseStatus.OK:
            raise APIError(
                f"An error occured while attempting to set the state of {name}"
            )
        return dataclass_from_dict(ACState, response.json())
