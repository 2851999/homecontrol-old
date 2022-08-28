import requests

from homecontrol.client.structs import APIConnectionInfo
from homecontrol.session import SessionWrapper


class APISession(SessionWrapper):
    """
    For handling a session for communicating with the api
    """

    _connection_info: APIConnectionInfo
    _session: requests.Session

    def __init__(self, connection_info: APIConnectionInfo) -> None:
        super().__init__(f"http://{connection_info.ip_address}:{connection_info.port}")
        self._connection_info = connection_info

    def _handle_start(self):
        """
        Sets up a session
        """
        # Add api key if required
        if self._connection_info.auth_required:
            self._session.headers.update({"X-Api-Key": self._connection_info.auth_key})

        return self
