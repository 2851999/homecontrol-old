from typing import Dict
from homecontrol.client.structs import APIConnectionInfo

from homecontrol.config import Config


class ClientConfig:
    """
    Handles the hue.json config
    """

    data: Dict

    def __init__(self) -> None:
        self.load()

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

    def save(self):
        """
        Saves the config
        """
        Config.save_to_json("client.json", self.data)

    def load(self):
        """
        Load the config
        """
        self.data = Config.load_from_json("client.json")
