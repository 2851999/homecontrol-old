from typing import Dict
from homecontrol.helpers import ResponseStatus
from homecontrol.hue.exceptions import HueAPIError
from homecontrol.hue.session import HueBridgeSession
from homecontrol.hue.structs import HueRoom


class Room:
    """
    Handles Philips Hue Room endpoints
    """

    _session: HueBridgeSession

    def __init__(self, session: HueBridgeSession) -> None:
        self._session = session

    def get_rooms(self) -> Dict[str, HueRoom]:
        """
        Returns a dictionary of rooms where keys represent the room name
        and the values their id
        """
        room_dict = {}
        response = self._session.get("/clip/v2/resource/room")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get rooms. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        # Obtain the data
        data = response.json()["data"]

        # Data should be a list of rooms
        for room in data:
            room_id = room["id"]
            room_name = room["metadata"]["name"]

            # Attempt to get a light group
            light_group = None
            for service in room["services"]:
                if service["rtype"] == "grouped_light":
                    light_group = service["rid"]
            devices = []
            for child in room["children"]:
                if child["rtype"] == "device":
                    devices.append(child["rid"])

            room_dict.update(
                {
                    room_name: HueRoom(
                        identifier=room_id, light_group=light_group, devices=devices
                    )
                }
            )

        return room_dict
