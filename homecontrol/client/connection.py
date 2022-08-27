import requests
from homecontrol.client.aircon import Aircon
from homecontrol.client.session import APISession

from homecontrol.client.structs import APIConnectionInfo


class APIConnection:
    """
    For handling a connection and proving access to the api
    """

    _session: APISession
    aircon: Aircon

    def __init__(self, connection_info: APIConnectionInfo) -> None:
        self._session = APISession(connection_info)

    def __enter__(self):
        self._session.start()

        self.aircon = Aircon(self._session)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._session.close()
