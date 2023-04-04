from datetime import datetime
from typing import List
from homecontrol.api.monitoring import TempDataPoint
from homecontrol.client.client import Client
from homecontrol.database.database import Database


def get_all_room_data():
    data = {}

    client = Client()
    with client.start_session() as session:
        data["outdoor"] = session.monitoring.get_temps("outdoor")
        for room in session.home.list_rooms("Home"):
            if room.ac_device_name is not None:
                data[room.name] = session.monitoring.get_temps(room.ac_device_name)
    return data


def parse_data(data: List[TempDataPoint]):
    x_values = []
    y_values = []
    for value in data:
        x_values.append(datetime.strptime(value.timestamp, Database.DATETIME_FORMAT))
        y_values.append(value.temp)
    return x_values, y_values


print(parse_data(get_all_room_data()["outdoor"]))
