from abc import ABC, abstractmethod

import requests


class SessionWrapper(ABC):
    """
    Used for handling a requests.Session object
    and providing easier access to API endpoints
    """

    _session: requests.Session
    _base_url: str

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url

    def start(self):
        """
        Assigns and sets up a session
        """
        self._session = requests.Session()
        self._handle_start()

    @abstractmethod
    def _handle_start(self):
        """
        Function called after a session is created for setting
        up any headers etc
        """

    def close(self):
        """
        Closes a session
        """
        self._session.close()

    def get(self, endpoint: str, **kwargs):
        """
        Returns the result of a get request
        """
        return self._session.get(f"{self._base_url}{endpoint}", **kwargs)

    def put(self, endpoint: str, **kwargs):
        """
        Returns the result of a put request
        """
        return self._session.put(f"{self._base_url}{endpoint}", **kwargs)

    def post(self, endpoint: str, **kwargs):
        """
        Returns the result of a post request
        """
        return self._session.post(f"{self._base_url}{endpoint}", **kwargs)
