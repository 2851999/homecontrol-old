from datetime import datetime
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from homecontrol.aircon.config import ACConfig

from homecontrol.client.client import Client
from homecontrol.database.database import Database
from homecontrol.scheduling.config import SchedulerConfig
from homecontrol.scheduling.structs import SchedulerMonitoringConfig


class Monitor:
    # Client interface
    client: Client

    # Config for monitoring
    monitoring_config: SchedulerMonitoringConfig

    # Database for storage
    database: Database

    def __init__(self, scheduler_config: SchedulerConfig):
        self.client = Client()
        self.monitoring_config = scheduler_config.get_monitoring()
        self.database = Database(scheduler_config.get_database())

    def add_jobs(self, scheduler: BlockingScheduler):
        if self.monitoring_config.enabled:
            scheduler.add_job(
                self.log_temps,
                CronTrigger.from_crontab(
                    self.monitoring_config.temperature_log_frequency
                ),
            )

    def init_db(self):
        """
        Initialises a database with the required tables for storing data
        """

        # Load AC device config
        ac_config = ACConfig()

        # Want list of AC devices for the tables
        devices = list(ac_config.get_devices().keys())
        devices.append("outdoor")

        # Connect to database
        with self.database.start_session() as db_conn:
            for device in devices:
                db_conn.create_table(
                    Database.clean_string(device) + "_temps",
                    ["timestamp TEXT", "temp REAL"],
                )

            db_conn.commit()

    def log_temps(self):
        """
        Logs temperatures from the air conditioning devices
        """

        with self.client.start_session() as hc_conn:
            loaded_devices = hc_conn.aircon.list_devices()

            # Obtain current date and time
            timestamp = datetime.now().strftime(Database.DATETIME_FORMAT)

            # Open connection to the database
            with self.database.start_session() as db_conn:
                # Outdoor temp (for now will only take first one)
                outdoor_temp = None

                for loaded_device in loaded_devices:
                    state = hc_conn.aircon.get_device(loaded_device)

                    db_conn.insert_values(
                        f"{Database.clean_string(loaded_device)}_temps",
                        [(timestamp, state.indoor)],
                    )

                    if outdoor_temp is None:
                        outdoor_temp = state.outdoor

                # Output outdoor temp
                db_conn.insert_values("outdoor_temps", [(timestamp, outdoor_temp)])

                db_conn.commit()


def main():
    scheduler_config = SchedulerConfig()
    monitor = Monitor(scheduler_config)

    # Check if just being told to create any needed databases
    if len(sys.argv) == 2 and sys.argv[1] == "init-db":
        monitor.init_db()
    else:
        scheduler = BlockingScheduler()
        monitor.add_jobs(scheduler)

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
