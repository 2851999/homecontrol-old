from homecontrol.config import Config
from homecontrol.scheduling.structs import (
    SchedulerDatabaseConfig,
    SchedulerMonitoringConfig,
)


class SchedulerConfig(Config):
    """
    Handles the api.json config
    """

    def __init__(self) -> None:
        super().__init__("scheduler.json")

    def get_monitoring(self) -> SchedulerMonitoringConfig:
        """
        Returns a SchedulerDatabaseConfig from the loaded config
        """
        monitoring = self.data["monitoring"]
        monitoring_config = SchedulerMonitoringConfig(
            enabled=monitoring["enabled"],
            temperature_log_frequency=monitoring.get("temperature_log_frequency"),
        )

        # Check validity
        if monitoring_config.enabled:
            if monitoring_config.temperature_log_frequency is None:
                raise ValueError(
                    "Invalid scheduler config, must specify 'temperature_log_frequency' "
                    "when monitoring is enabled"
                )

        return monitoring_config

    def get_database(self) -> SchedulerDatabaseConfig:
        """
        Returns a SchedulerDatabaseConfig from the loaded config
        """
        database = self.data["database"]
        return SchedulerDatabaseConfig(path=database["path"])
