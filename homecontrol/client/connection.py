from homecontrol.client.aircon import Aircon
from homecontrol.client.auth import Auth
from homecontrol.client.home import Home
from homecontrol.client.hue import Hue
from homecontrol.client.info import Info
from homecontrol.client.monitoring import Monitoring
from homecontrol.client.session import APISession
from homecontrol.client.structs import APIConnectionConfig


class APIConnection:
    """
    For handling a connection and proving access to the api
    """

    _session: APISession
    auth: Auth
    aircon: Aircon
    hue: Hue
    home: Home
    info: Info
    monitoring: Monitoring

    def __init__(self, connection_config: APIConnectionConfig) -> None:
        self._session = APISession(connection_config)

    def __enter__(self):
        self._session.start()

        self.auth = Auth(self._session)
        self.aircon = Aircon(self._session)
        self.hue = Hue(self._session)
        self.home = Home(self._session)
        self.info = Info(self._session)
        self.monitoring = Monitoring(self._session)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._session.close()
