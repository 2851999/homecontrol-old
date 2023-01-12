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


def construct_monitor_api_blueprint(monitoring_info: APIMonitoringInfo):
    """
    Creates a blueprint for the monitoring API
    """

    monitor_api = Blueprint("monitor_api", __name__)

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
