from dataclasses import dataclass
from datetime import datetime
from typing import List
from flask import Blueprint, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from homecontrol.aircon.manager import ACManager
from homecontrol.api.helpers import authenticated, response
from homecontrol.api.structs import APIMonitoringInfo
from homecontrol.helpers import ResponseStatus


@dataclass
class TempDataPoint:
    """
    For storing a temperature data point
    """

    timestamp: str
    temp: float


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

    def get_temp_data(self, device_name) -> List[TempDataPoint]:
        """
        Returns logged temperature data for a device
        """
        log_path = f"{self.monitoring_info.temperature_log_path}/{device_name}.csv"

        # Obtain the data
        data = []

        with open(log_path, "r", encoding="utf-8") as file:
            for line in file:
                split = line.split(",")
                data.append(TempDataPoint(timestamp=split[0], temp=float(split[1])))

        return data

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


def construct_monitor_api_blueprint(monitor: Monitor):
    """
    Creates a blueprint for the monitoring API
    """

    monitor_api = Blueprint("monitor_api", __name__)

    @monitor_api.route("/monitoring/temps", methods=["GET"])
    @authenticated
    def get_temps():
        """
        Returns data about logged temperatures of a particular AC unit
        """
        args = request.args

        # Get the bridge name
        device_name = args.get("device_name")

        # Obtain the data
        data = monitor.get_temp_data(device_name)

        # Return the response
        return response(data, ResponseStatus.OK)

    return monitor_api
