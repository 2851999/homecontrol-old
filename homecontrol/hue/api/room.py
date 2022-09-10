from typing import List
from homecontrol.helpers import ResponseStatus, dicts_to_list, object_to_dict
from homecontrol.hue.api.structs import RoomGet, RoomPut
from homecontrol.hue.exceptions import HueAPIError
from homecontrol.hue.session import HueBridgeSession


class Room:
    """
    Handles Philips Hue Room endpoints
    """

    _session: HueBridgeSession

    def __init__(self, session: HueBridgeSession) -> None:
        self._session = session

    def get_rooms(self) -> List[RoomGet]:
        """
        Returns a list of rooms
        """
        response = self._session.get("/clip/v2/resource/room")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get rooms. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        # Obtain the data
        data = response.json()["data"]
        return dicts_to_list(RoomGet, data)

    def get_room(self, identifier: str) -> RoomGet:
        """
        Returns a room
        """
        response = self._session.get(f"/clip/v2/resource/room/{identifier}")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get status of room with id {identifier}. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        # Obtain the data
        data = response.json()["data"]
        return dicts_to_list(RoomGet, data)[0]

    def put_room(self, identifier: str, room_put: RoomPut):
        """
        Attempts to assign the state of a room
        """

        response = self._session.put(
            f"/clip/v2/resource/room/{identifier}",
            json=object_to_dict(room_put),
        )

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to update the room with id {identifier} "
                f"Status code: {response.status_code}. Content {response.content}."
            )
