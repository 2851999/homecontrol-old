from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from homecontrol.aircon.manager import ACManager
from homecontrol.api.structs import APIMonitoringInfo


class Monitor:
    """
    Handles monitoring
    """

    def __init__(self, ac_manager: ACManager, monitoring_info: APIMonitoringInfo):
        # Assign the ACManager
        self.ac_manager = ac_manager
        self.monitoring_info = monitoring_info

        # Add jobs if enabled
        if monitoring_info.enabled:
            scheduler = BackgroundScheduler()

            # scheduler.add_job(self.log_temps, "interval", seconds=5)
            scheduler.add_job(
                self.log_temps,
                CronTrigger.from_crontab(monitoring_info.temperature_log_frequency),
            )
            scheduler.start()

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
        loaded_devices = self.ac_manager.list_devices()

        # Obtain current date and time
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Outdoor temp (for now will only take first one)
        outdoor_temp = None

        for loaded_device in loaded_devices:
            device = self.ac_manager.get_device(loaded_device)
            state = device.get_state()

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
