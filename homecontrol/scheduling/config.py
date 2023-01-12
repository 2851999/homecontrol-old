from homecontrol.config import Config
from homecontrol.scheduling.structs import SchedulerMonitoringInfo


class SchedulerConfig(Config):
    """
    Handles the api.json config
    """

    def __init__(self) -> None:
        super().__init__("scheduler.json")

    def get_monitoring(self) -> SchedulerMonitoringInfo:
        """
        Returns a APIMonitoringInfo from the loaded config
        """
        monitoring = self.data["monitoring"]
        monitoring_info = SchedulerMonitoringInfo(
            enabled=monitoring["enabled"],
            temperature_log_path=monitoring.get("temperature_log_path"),
            temperature_log_frequency=monitoring.get("temperature_log_frequency"),
        )

        # Check validity
        if monitoring_info.enabled:
            if monitoring_info.temperature_log_path is None:
                raise ValueError(
                    "Invalid scheduler config, must specify 'temperature_log_path' "
                    "when monitoring is enabled"
                )
            if monitoring_info.temperature_log_frequency is None:
                raise ValueError(
                    "Invalid scheduler config, must specify 'temperature_log_frequency' "
                    "when monitoring is enabled"
                )

        return monitoring_info
