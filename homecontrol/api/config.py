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
            enabled=monitoring["enabled"],
            temperature_log_path=monitoring.get("temperature_log_path"),
            temperature_log_frequency=monitoring.get("temperature_log_frequency"),
        )

        # Check validity
        if monitoring_info.enabled:
            if monitoring_info.temperature_log_path is None:
                raise ValueError(
                    "Invalid API config, must specify 'temperature_log_path' "
                    "when monitoring is enabled"
                )
            if monitoring_info.temperature_log_frequency is None:
                raise ValueError(
                    "Invalid API config, must specify 'temperature_log_frequency' "
                    "when monitoring is enabled"
                )

        return monitoring_info
