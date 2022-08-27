from typing import List, Optional
from homecontrol.api.structs import ResponseStatus
from homecontrol.client.exceptions import APIError
from homecontrol.client.session import APISession


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
