from dataclasses import dataclass
from typing import List
from flask import Blueprint, request

from homecontrol.api.helpers import authenticated, response
from homecontrol.helpers import ResponseStatus
from homecontrol.scheduling.config import SchedulerConfig


@dataclass
class TempDataPoint:
    """
    For storing a temperature data point
    """

    timestamp: str
    temp: float


def construct_monitor_api_blueprint():
    """
    Creates a blueprint for the monitoring API
    """

    monitor_api = Blueprint("monitor_api", __name__)

    # Obtain the scheduling config (so can obtain monitoring log paths)
    scheduler_config = SchedulerConfig()
    monitoring_info = scheduler_config.get_monitoring()

    def get_temp_data(device_name) -> List[TempDataPoint]:
        """
        Returns logged temperature data for a device
        """
        log_path = f"{monitoring_info.temperature_log_path}/{device_name}.csv"

        # Obtain the data
        data = []

        with open(log_path, "r", encoding="utf-8") as file:
            for line in file:
                split = line.split(",")
                data.append(TempDataPoint(timestamp=split[0], temp=float(split[1])))

        return data

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
        data = get_temp_data(device_name)

        # Return the response
        return response(data, ResponseStatus.OK)

    return monitor_api
