from homecontrol.api.structs import APIAuthInfo, APIMonitoringInfo

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

    def get_monitoring(self) -> APIMonitoringInfo:
        """
        Returns a APIMonitoringInfo from the loaded config
        """
        monitoring = self.data["monitoring"]
        monitoring_info = APIMonitoringInfo(
            temperature_log_path=monitoring.get("temperature_log_path"),
        )

        return monitoring_info
