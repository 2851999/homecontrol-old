from typing import List
from homecontrol.hue.api.api import HueBridgeAPI
from homecontrol.hue.structs import HueRoom


class Room:
    """
    Handles Philips Hue Room endpoints
    """

    _api: HueBridgeAPI

    def __init__(self, api: HueBridgeAPI) -> None:
        self._api = api

    def get_rooms(self) -> List[HueRoom]:
        """
        Returns a dictionary of rooms where keys represent the room name
        and the values their id
        """
        rooms = self._api.room.get_rooms()
        # Convert to the room structure we actually want to return
        room_list = []
        # Data should be a list of rooms
        for room in rooms:

            # Attempt to get a light group
            light_group = None
            for service in room.services:
                if service.rtype == "grouped_light":
                    light_group = service.rid
            lights = []
            for child in room.children:
                if child.rtype == "device":
                    # Query the device
                    device_info = self._api.device.get_device(child.rid)
                    for service in device_info.services:
                        if service.rtype == "light":
                            lights.append(child.rid)

            room_list.append(
                HueRoom(
                    identifier=room.id,
                    name=room.metadata.name,
                    light_group=light_group,
                    lights=lights,
                )
            )
        return room_list
