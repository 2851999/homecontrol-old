from typing import List, Optional

import requests

from homecontrol.hue.connection import HueBridgeConnection
from homecontrol.hue.structs import HueBridgeAuthConfig, HueBridgeConnectionConfig


class HueBridge:
    """
    Refers to a hue bridge
    """

    # URL for discovering bridges
    DISCOVERY_URL: str = "https://discovery.meethue.com/"

    _ca_cert: str
    _connection_config: HueBridgeConnectionConfig
    _connection_auth: Optional[HueBridgeAuthConfig]

    def __init__(
        self,
        ca_cert: str,
        connection_config: HueBridgeConnectionConfig,
        connection_auth: Optional[HueBridgeAuthConfig] = None,
    ) -> None:
        """
        Creates the msmart device instance and authenticates it
        """
        self._ca_cert = ca_cert
        self._connection_config = connection_config
        self._connection_auth = connection_auth

    def start_session(self) -> HueBridgeConnection:
        """
        Returns a HueBridgeConnection instance for contacting the bridge
        e.g. 'with bridge.start_session() as session'
        """
        return HueBridgeConnection(
            connection_config=self._connection_config,
            ca_cert=self._ca_cert,
            auth_config=self._connection_auth,
        )

    @staticmethod
    def discover() -> List[HueBridgeConnectionConfig]:
        """
        Obtains connection information for a hue bridge

        :raises ConnectionError: When there is a connection issue
        """

        response = requests.get(url=HueBridge.DISCOVERY_URL)
        if response.status_code == 200:
            bridges = response.json()
            bridges_conn_info = []
            for bridge in bridges:
                bridges_conn_info.append(
                    HueBridgeConnectionConfig(
                        identifier=bridge["id"],
                        ip_address=bridge["internalipaddress"],
                        port=bridge["port"],
                    )
                )
            return bridges_conn_info
        raise ConnectionError(
            f"An error occurred trying to discover bridges. "
            f"The status code received was {response.status_code}."
        )
