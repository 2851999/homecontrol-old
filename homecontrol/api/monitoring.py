from dataclasses import dataclass
import os
from typing import List, Optional
from flask import Blueprint, request
from homecontrol.api.data_utils import read_all_lines, read_last_lines

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
    monitoring_config = scheduler_config.get_monitoring()

    def _temp_data_parse_func(line: str):
        split = line.split(",")
        return TempDataPoint(timestamp=split[0], temp=float(split[1]))

    def _get_temp_data(
        device_name: str, count: Optional[int], step: Optional[int]
    ) -> List[TempDataPoint]:
        """
        Returns logged temperature data for a device
        """
        log_path = f"{monitoring_config.temperature_log_path}/{device_name}.csv"

        # Obtain the data
        if count is None:
            return read_all_lines(log_path, step, _temp_data_parse_func)
        else:
            return read_last_lines(log_path, count, step, _temp_data_parse_func)

    @monitor_api.route("/monitoring/temps", methods=["GET"])
    @authenticated
    def get_temps():
        """
        Returns data logged temperature data of a particular AC unit
        """
        args = request.args

        # Get the bridge name
        device_name = args.get("device_name")

        # Could use filters here to modify data returned, but for now will do
        # separately as want to hijack and modify how data is loaded in the
        # first place rather than modify it afterwards
        count = request.args.get("count", None, type=int)
        step = request.args.get("step", None, type=int)

        # Obtain the data
        data = _get_temp_data(device_name, count, step)

        # Return the response
        return response(data, ResponseStatus.OK)

    return monitor_api
