from typing import List, Optional

from homecontrol.aircon.structs import ACState
from homecontrol.client.helpers import check_response
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
        check_response(response, "An error occurred listing devices")
        return response.json()

    def register_device(
        self, name: str, ip_address: str, retries: Optional[int] = None
    ) -> bool:
        """
        Registers a device with the API

        Args:
            name (str): Name of the device to register
            ip_address (str): IP address of the device to register
            retries (Optional[int]): Number of times to try
        Returns:
            bool: Whether registration was successful or not
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
        check_response(response, f"An error occurred getting the state of {name}")
        return dataclass_from_dict(ACState, response.json())

    def set_device(self, name: str, state: ACState) -> ACState:
        """
        Sets the state of a device
        """
        response = self._session.put(f"/ac/devices/{name}", json=state.__dict__)
        check_response(
            response, f"An error occurred while attempting to set the state of {name}"
        )
        return dataclass_from_dict(ACState, response.json())
