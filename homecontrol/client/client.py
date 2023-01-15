from homecontrol.client.config import ClientConfig
from homecontrol.client.connection import APIConnection


class Client:
    """
    Class for handling requests for the API
    """

    _config: ClientConfig

    def __init__(self) -> None:
        self._config = ClientConfig()

    def start_session(self) -> APIConnection:
        """
        Returns an APIConnection instance for contacting the homecontrol API
        e.g. 'with client.start_session() as session'
        """
        return APIConnection(
            connection_config=self._config.get_api_connection_config(),
        )
