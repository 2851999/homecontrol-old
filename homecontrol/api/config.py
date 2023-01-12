from homecontrol.api.structs import APIAuthInfo

from homecontrol.config import Config


class APIConfig(Config):
    """
    Handles the api.json config
    """

    def __init__(self) -> None:
        super().__init__("api.json")

    def get_auth(self) -> APIAuthInfo:
        """
        Returns a APIAuthInfo from the loaded config
        """
        auth = self.data["auth"]
        return APIAuthInfo(required=auth["required"], key=auth["key"])
