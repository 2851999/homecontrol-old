import requests

from homecontrol.client.structs import APIConnectionInfo


class APISession:
    """
    For handling a session for communicating with the api
    """

    _connection_info: APIConnectionInfo
    _session: requests.Session
    _url: str

    def __init__(self, connection_info: APIConnectionInfo) -> None:
        self._connection_info = connection_info
        self._url = (
            f"http://{self._connection_info.ip_address}:{self._connection_info.port}"
        )

    def start(self):
        """
        Assigns and sets up a session
        """
        self._session = requests.Session()
        # Add api key if required
        if self._connection_info.auth_required:
            self._session.headers.update({"X-Api-Key": self._connection_info.auth_key})

        return self

    def close(self):
        """
        Closes a session
        """
        self._session.close()

    def get(self, endpoint: str, **kwargs):
        """
        Returns the result of a get request
        """
        return self._session.get(f"{self._url}{endpoint}", **kwargs)

    def put(self, endpoint: str, **kwargs):
        """
        Returns the result of a put request
        """
        return self._session.put(f"{self._url}{endpoint}", **kwargs)

    def post(self, endpoint: str, **kwargs):
        """
        Returns the result of a post request
        """
        return self._session.post(f"{self._url}{endpoint}", **kwargs)
