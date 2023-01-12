from dataclasses import dataclass
from typing import Optional


@dataclass
class SchedulerMonitoringInfo:
    """
    Stores monitoring config for the scheduler
    """

    enabled: bool
    temperature_log_path: Optional[str]
    temperature_log_frequency: Optional[str]
