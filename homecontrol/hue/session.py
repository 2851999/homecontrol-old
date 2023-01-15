from typing import Optional
import requests
from requests_toolbelt.adapters import host_header_ssl

from homecontrol.hue.structs import HueBridgeAuthConfig, HueBridgeConnectionConfig
from homecontrol.session import SessionWrapper


class HueBridgeSession(SessionWrapper):
    """
    For handling a session for communicating with a hue bridge
    """

    _connection_config: HueBridgeConnectionConfig
    _ca_cert: str
    _auth_config: Optional[HueBridgeAuthConfig]
    _session: requests.Session

    def __init__(
        self,
        connection_config: HueBridgeConnectionConfig,
        ca_cert: str,
        auth_config: Optional[HueBridgeAuthConfig] = None,
    ) -> None:
        super().__init__(
            f"https://{connection_config.ip_address}:{connection_config.port}"
        )

        self._connection_config = connection_config
        self._ca_cert = ca_cert
        self._auth_config = auth_config

    def _handle_start(self):
        """
        Sets up a session
        """
        # Solve SSLCertVerificationError due to difference in hostname
        self._session.mount("https://", host_header_ssl.HostHeaderSSLAdapter())
        self._session.headers.update({"Host": f"{self._connection_config.identifier}"})
        # Add acutal auth key if have it
        if self._auth_config is not None:
            self._session.headers.update(
                {"hue-application-key": self._auth_config.username}
            )
        self._session.verify = self._ca_cert

        return self
