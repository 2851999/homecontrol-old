from typing import Dict
from homecontrol.api.structs import APIAuthInfo

from homecontrol.config import Config


class APIConfig:
    """
    Handles the api.json config
    """

    data: Dict

    def __init__(self) -> None:
        self.load()

    def get_auth(self) -> APIAuthInfo:
        """
        Returns a APIAuthInfo from the loaded config
        """
        auth = self.data["auth"]
        return APIAuthInfo(required=auth["required"], key=auth["key"])

    def save(self):
        """
        Saves the config
        """
        Config.save_to_json("api.json", self.data)

    def load(self):
        """
        Load the config
        """
        self.data = Config.load_from_json("api.json")
