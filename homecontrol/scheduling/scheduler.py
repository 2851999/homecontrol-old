from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from homecontrol.api.structs import APIMonitoringInfo
from homecontrol.client.client import Client
from homecontrol.scheduling.config import SchedulerConfig
from homecontrol.scheduling.structs import SchedulerMonitoringInfo


class Monitor:
    # Client interface
    client: Client

    # Config for monitoring
    monitoring_info: APIMonitoringInfo

    def __init__(
        self, scheduler: BlockingScheduler, monitoring_info: SchedulerMonitoringInfo
    ):
        self.client = Client()
        self.monitoring_info = monitoring_info

        if monitoring_info.enabled:
            scheduler.add_job(
                self.log_temps,
                CronTrigger.from_crontab(monitoring_info.temperature_log_frequency),
            )

    def append_to_file(self, filepath, value):
        """
        Appends a line onto a given file
        """
        with open(filepath, "a", encoding="utf-8") as file:
            file.write(f"{value}\n")

    def log_temps(self):
        """
        Logs temperatures from the air conditioning devices
        """
        with self.client.start_session() as conn:
            loaded_devices = conn.aircon.list_devices()

            # Obtain current date and time
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            # Outdoor temp (for now will only take first one)
            outdoor_temp = None

            for loaded_device in loaded_devices:
                state = conn.aircon.get_device(loaded_device)

                # Log path
                log_path = (
                    f"{self.monitoring_info.temperature_log_path}/{loaded_device}.csv"
                )

                log_value = f"{timestamp},{state.indoor}"
                self.append_to_file(log_path, log_value)

                if outdoor_temp is None:
                    outdoor_temp = state.outdoor

            # Output outdoor temp
            log_path = f"{self.monitoring_info.temperature_log_path}/outdoor.csv"
            log_value = f"{timestamp},{outdoor_temp}"
            self.append_to_file(log_path, log_value)


def start():
    scheduler_config = SchedulerConfig()
    monitoring_info = scheduler_config.get_monitoring()

    scheduler = BlockingScheduler()

    _monitor = Monitor(scheduler, monitoring_info)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
