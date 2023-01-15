from dataclasses import dataclass
import os
from typing import List, Optional
from flask import Blueprint, request

from homecontrol.api.helpers import authenticated, response
from homecontrol.database.database import Database
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

    database = Database(scheduler_config.get_database())

    def _get_temp_data(
        device_name: str, count: Optional[int], step: Optional[int]
    ) -> List[TempDataPoint]:
        """
        Returns logged temperature data for a device
        """
        table_name = f"{Database.clean_string(device_name)}_temps"
        limit = count if count is not None else None
        # Need more data if taking step
        if step is not None and limit:
            limit *= step

        # Obtain the data
        with database.start_session() as db_conn:
            data = db_conn.select_values(
                table_name,
                ["timestamp", "temp"],
                limit=limit
                # where="timestamp BETWEEN '2023-01-12 22:00:00' AND '2023-01-13 00:00:00'",
            )

            # Apply step
            if step is not None:
                data = data[::step]

            # Convert to expected structs
            struct_data = []
            for data_value in data:
                struct_data.append(TempDataPoint(data_value[0], data_value[1]))

            return struct_data

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
        # separately as want to hijack and modify how data obtained in the
        # first place rather than modify it afterwards
        count = request.args.get("count", None, type=int)
        step = request.args.get("step", None, type=int)

        # Obtain the data
        data = _get_temp_data(device_name, count, step)

        # Return the response
        return response(data, ResponseStatus.OK)

    return monitor_api
