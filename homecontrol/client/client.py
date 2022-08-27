import requests

from homecontrol.client.config import ClientConfig
from homecontrol.client.structs import APIConnectionInfo


class APIConnection:
    """
    For handling a session for communicating with the api
    """

    connection_info: APIConnectionInfo
    session: requests.Session
    url: str

    def __init__(self, connection_info: APIConnectionInfo) -> None:
        self.connection_info = connection_info
        self.url = (
            f"http://{self.connection_info.ip_address}:{self.connection_info.port}"
        )

    def __enter__(self):
        self.session = requests.Session()
        # Add api key if required
        if self.connection_info.auth_required:
            self.session.headers.update({"X-Api-Key": self.connection_info.auth_key})

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.session.close()

    def get(self, endpoint: str, **kwargs):
        """
        Returns the result of a get request
        """
        return self.session.get(f"{self.url}{endpoint}", **kwargs)

    def put(self, endpoint: str, **kwargs):
        """
        Returns the result of a put request
        """
        return self.session.put(f"{self.url}{endpoint}", **kwargs)

    def post(self, endpoint: str, **kwargs):
        """
        Returns the result of a post request
        """
        return self.session.post(f"{self.url}{endpoint}", **kwargs)


class Client:
    """
    Class for handling requests for the API
    """

    config: ClientConfig

    def __init__(self) -> None:
        self.config = ClientConfig()

    def start_session(self):
        """
        Returns an APISession instance for contacting the homecontrol API
        e.g. 'with client.start_session() as session'
        """
        return APIConnection(
            connection_info=self.config.get_api_connection_info(),
        )
