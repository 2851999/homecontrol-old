from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from flask import Blueprint, request

from homecontrol.api.helpers import authenticated, response
from homecontrol.database.sqlite.database import Database
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

    # Obtain the scheduling config (needed to access the database)
    scheduler_config = SchedulerConfig()

    database = Database(scheduler_config.get_database())

    def _get_temp_data(
        device_name: str,
        count: Optional[int],
        step: Optional[int],
        start: Optional[str],
        end: Optional[str],
    ) -> List[TempDataPoint]:
        """
        Returns logged temperature data for a device
        """
        table_name = f"{Database.clean_string(device_name)}_temps"
        limit = count if count is not None else None
        # Need more data if taking step
        if step is not None and limit:
            limit *= step

        where = None
        if start is not None and end is not None:
            where = [f"timestamp BETWEEN ? AND ?", (start, end)]
        elif start is not None:
            where = [f"timestamp >= ?", (start,)]
        elif end is not None:
            where = [f"timestamp <= ?", (end,)]

        # Obtain the data
        with database.start_session() as db_conn:
            data = db_conn.select_values(
                table_name, ["timestamp", "temp"], limit=limit, where=where
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
        start = request.args.get("start", None, type=str)
        end = request.args.get("end", None, type=str)

        def convert_to_datetime(value: Optional[str]):
            """Throws ValueError if not valid"""
            if value is not None:
                return datetime.strptime(value, Database.DATETIME_FORMAT)
            return value

        # Ensure the start and end timestamps are valid
        try:
            start = convert_to_datetime(start)
            end = convert_to_datetime(end)
        except ValueError:
            return response(
                "Invalid 'start' or 'end' date given", ResponseStatus.BAD_REQUEST
            )

        # Obtain the data
        data = _get_temp_data(device_name, count, step, start, end)

        # Return the response
        return response(data, ResponseStatus.OK)

    return monitor_api
