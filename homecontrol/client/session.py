import requests

from homecontrol.client.structs import APIConnectionConfig
from homecontrol.session import SessionWrapper


class APISession(SessionWrapper):
    """
    For handling a session for communicating with the api
    """

    _connection_config: APIConnectionConfig
    _session: requests.Session

    def __init__(self, connection_config: APIConnectionConfig) -> None:
        super().__init__(
            f"http://{connection_config.ip_address}:{connection_config.port}"
        )
        self._connection_config = connection_config

    def _handle_start(self):
        """
        Sets up a session
        """
        # Add api key if required
        if self._connection_config.auth_required:
            self._session.headers.update(
                {"X-Api-Key": self._connection_config.auth_key}
            )

        return self
