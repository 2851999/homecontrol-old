from typing import Any, List, Optional, Type

import requests
from requests_toolbelt.adapters import host_header_ssl

from homecontrol.helpers import ResponseStatus, dicts_to_list, object_to_dict
from homecontrol.hue.api.exceptions import HueAPIError
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
        # Add actual auth key if have it
        if self._auth_config is not None:
            self._session.headers.update(
                {"hue-application-key": self._auth_config.username}
            )
        self._session.verify = self._ca_cert

        return self

    def get_resource(self, endpoint: str, class_type: Type, error_message: str) -> List:
        """
        Returns data from an endpoint
        """
        response = self.get(endpoint)

        if response.status_code != ResponseStatus.OK:
            print(response.content)
            raise HueAPIError(
                f"{error_message} "
                f"Status code: {response.status_code}. Content {response.content}."
            )
        data = response.json()["data"]
        return dicts_to_list(class_type, data)

    def put_resource(self, endpoint: str, obj: Any, error_message: str):
        """
        Performs a put request for a resource
        """

        response = self.put(
            endpoint,
            json=object_to_dict(obj),
        )

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"{error_message} "
                f"Status code: {response.status_code}. Content {response.content}."
            )
