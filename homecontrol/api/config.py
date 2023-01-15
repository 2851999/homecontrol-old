from homecontrol.api.structs import APIAuthConfig

from homecontrol.config import Config


class APIConfig(Config):
    """
    Handles the api.json config
    """

    def __init__(self) -> None:
        super().__init__("api.json")

    def get_auth(self) -> APIAuthConfig:
        """
        Returns a APIAuthConfig from the loaded config
        """
        auth = self.data["auth"]
        return APIAuthConfig(required=auth["required"], key=auth["key"])
