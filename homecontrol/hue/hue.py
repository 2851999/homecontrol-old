from typing import List, Optional
import requests
from homecontrol.hue.bridge_structs import HueBridgeAuthInfo, HueBridgeConnectionInfo
from homecontrol.hue.connection import HueBridgeConnection


HUE_BRIDGE_DISCOVERY_URL = "https://discovery.meethue.com/"


class HueBridge:
    """
    Refers to a hue bridge
    """

    _ca_cert: str
    _connection_info: HueBridgeConnectionInfo
    _connection_auth: Optional[HueBridgeAuthInfo]

    def __init__(
        self,
        ca_cert: str,
        connection_info: HueBridgeConnectionInfo,
        connection_auth: Optional[HueBridgeAuthInfo] = None,
    ) -> None:
        """
        Creates the msmart device instance and authenticates it
        """
        self._ca_cert = ca_cert
        self._connection_info = connection_info
        self._connection_auth = connection_auth

    def start_session(self) -> HueBridgeConnection:
        """
        Returns a HueBridgeConnection instance for contacting the bridge
        e.g. 'with bridge.start_session() as session'
        """
        return HueBridgeConnection(
            connection_info=self._connection_info,
            ca_cert=self._ca_cert,
            auth_info=self._connection_auth,
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
