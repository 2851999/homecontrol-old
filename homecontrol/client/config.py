from typing import Dict
from homecontrol.client.structs import APIConnectionInfo

from homecontrol.config import Config


class ClientConfig(Config):
    """
    Handles the client.json config
    """

    def __init__(self) -> None:
        super().__init__("client.json")

    def get_api_connection_info(self) -> APIConnectionInfo:
        """
        Returns APIConnectionInfo from the config
        """
        return APIConnectionInfo(
            auth_required=self.data["api"]["auth"]["required"],
            auth_key=self.data["api"]["auth"]["key"],
            ip_address=self.data["api"]["ip"],
            port=self.data["api"]["port"],
        )
