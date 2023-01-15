from datetime import datetime
import re
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from homecontrol.client.client import Client
from homecontrol.database.database import Database
from homecontrol.scheduling.config import SchedulerConfig
from homecontrol.scheduling.structs import SchedulerMonitoringInfo


class Monitor:
    # Client interface
    client: Client

    # Config for monitoring
    monitoring_info: SchedulerMonitoringInfo

    def __init__(self, monitoring_info: SchedulerMonitoringInfo):
        self.client = Client()
        self.monitoring_info = monitoring_info

    def add_jobs(self, scheduler: BlockingScheduler):
        if self.monitoring_info.enabled:
            scheduler.add_job(
                self.log_temps,
                CronTrigger.from_crontab(
                    self.monitoring_info.temperature_log_frequency
                ),
            )

    def clean_string(self, value):
        """
        Convert string into a valid variable name
        """
        # https://stackoverflow.com/questions/3303312/how-do-i-convert-a-string-to-a-valid-variable-name-in-python
        return re.sub(r"\W|^(?=\d)", "_", value)

    def init_db(self, database: Database):
        """
        Initialises a database with the required tables for storing data
        """

        # Want list of AC for the tables
        with self.client.start_session() as hc_conn:
            loaded_devices = hc_conn.aircon.list_devices()

            # Connect to database
            with database.start_session() as db_conn:
                for device in loaded_devices:
                    db_conn.create_table(
                        self.clean_string(device), "timestamp TEXT, temp REAL"
                    )
                db_conn.commit()

    def append_to_file(self, filepath: str, value: str):
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


def main():
    scheduler_config = SchedulerConfig()
    monitoring_info = scheduler_config.get_monitoring()
    monitor = Monitor(monitoring_info)

    database = Database(scheduler_config.get_database())

    # Check if just being told to create any needed databases
    if len(sys.argv) == 2 and sys.argv[1] == "init-db":
        monitor.init_db(database)
    else:
        scheduler = BlockingScheduler()
        monitor.add_jobs(scheduler)

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
