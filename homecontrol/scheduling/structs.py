from dataclasses import dataclass
from typing import Optional


@dataclass
class SchedulerMonitoringConfig:
    """
    Stores monitoring config for the scheduler
    """

    enabled: bool
    temperature_log_frequency: Optional[str]


@dataclass
class SchedulerDatabaseConfig:
    """
    Stores database config for the scheduler
    """

    path: str
