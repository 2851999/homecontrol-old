from enum import Enum
import sys
from typing import List, Optional
import requests
from requests_toolbelt.adapters import host_header_ssl
from homecontrol.hue.bridge_structs import HueBridgeAuthInfo, HueBridgeConnectionInfo

from homecontrol.hue.config import HueConfig


HUE_BRIDGE_DISCOVERY_URL = "https://discovery.meethue.com/"


class HueBridgeConnection:
    """
    Handles the connection to a hue bridge
    """

    connection_info: HueBridgeConnectionInfo
    ca_cert: str
    auth_info: Optional[HueBridgeAuthInfo]
    session: requests.Session
    url: str

    def __init__(
        self,
        connection_info: str,
        ca_cert: str,
        auth_info: Optional[HueBridgeAuthInfo] = None,
    ) -> None:
        """
        :param connection_info: HueBridgeConnectionInfo instance for the bridge
        :param ca_cert: Path to the CA certificate for authenticating with the bridge
        """
        self.connection_info = connection_info
        self.ca_cert = ca_cert
        self.auth_info = auth_info
        self.url = f"https://{self.connection_info.ip_address}"

    def __enter__(self):
        self.session = requests.Session()
        # Solve SSLCertVerificationError due to difference in hostname
        self.session.mount("https://", host_header_ssl.HostHeaderSSLAdapter())
        self.session.headers.update({"Host": f"{self.connection_info.identifier}"})
        # Add acutal auth key if have it
        if self.auth_info is not None:
            self.session.headers.update(
                {"hue-application-key": self.auth_info.username}
            )
        self.session.verify = self.ca_cert

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


class HueBridge:
    """
    Refers to a hue bridge
    """

    ca_cert: str
    connection_info: HueBridgeConnectionInfo
    connection: HueBridgeConnection
    connection_auth: Optional[HueBridgeAuthInfo]

    def __init__(
        self,
        ca_cert: str,
        connection_info: HueBridgeConnectionInfo,
        connection_auth: Optional[HueBridgeAuthInfo] = None,
    ) -> None:
        """
        Creates the msmart device instance and authenticates it
        """
        self.ca_cert = ca_cert
        self.connection_info = connection_info
        self.connection_auth = connection_auth

    def start_session(self):
        """
        Returns a HueBridgeConnection instance for contacting the bridge
        e.g. 'with bridge.start_session() as session'
        """
        return HueBridgeConnection(
            connection_info=self.connection_info,
            ca_cert=self.ca_cert,
            auth_info=self.connection_auth,
        )

    @staticmethod
    def discover() -> List[HueBridgeConnectionInfo]:
        """
        Obtains connection information for a hue bridge

        :raises ConnectionError: When there is a connection issue
        """

        response = requests.get(url=HUE_BRIDGE_DISCOVERY_URL)
        if response.status_code == 200:
            bridges = response.json()
            bridges_conn_info = []
            for bridge in bridges:
                bridges_conn_info.append(
                    HueBridgeConnectionInfo(
                        identifier=bridge["id"],
                        ip_address=bridge["internalipaddress"],
                        port=bridge["port"],
                    )
                )
            return bridges_conn_info
        raise ConnectionError(
            f"An error occured trying to discover bridges. "
            f"The status code recieved was {response.status_code}."
        )
