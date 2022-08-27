from typing import Optional
import requests
from requests_toolbelt.adapters import host_header_ssl

from homecontrol.hue.structs import HueBridgeAuthInfo, HueBridgeConnectionInfo


class HueBridgeSession:
    """
    For handling a session for communicating with a hue bridge
    """

    _connection_info: HueBridgeConnectionInfo
    _ca_cert: str
    _auth_info: Optional[HueBridgeAuthInfo]
    _session: requests.Session
    _url: str

    def __init__(
        self,
        connection_info: HueBridgeConnectionInfo,
        ca_cert: str,
        auth_info: Optional[HueBridgeAuthInfo] = None,
    ) -> None:
        self._connection_info = connection_info
        self._ca_cert = ca_cert
        self._auth_info = auth_info
        self._url = (
            f"https://{self._connection_info.ip_address}:{self._connection_info.port}"
        )

    def start(self):
        """
        Assigns and sets up a session
        """
        self._session = requests.Session()
        # Solve SSLCertVerificationError due to difference in hostname
        self._session.mount("https://", host_header_ssl.HostHeaderSSLAdapter())
        self._session.headers.update({"Host": f"{self._connection_info.identifier}"})
        # Add acutal auth key if have it
        if self._auth_info is not None:
            self._session.headers.update(
                {"hue-application-key": self._auth_info.username}
            )
        self._session.verify = self._ca_cert

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
