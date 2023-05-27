from typing import List

from homecontrol.hue.api.structs import RoomGet, RoomPut
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

        return self._session.get_resource(
            endpoint="/clip/v2/resource/room",
            class_type=RoomGet,
            error_message="An error occurred trying to get rooms.",
        )

    def get_room(self, identifier: str) -> RoomGet:
        """
        Returns a room
        """

        return self._session.get_resource(
            endpoint=f"/clip/v2/resource/room/{identifier}",
            class_type=RoomGet,
            error_message=f"An error occurred trying to get status of the room with id {identifier}.",
        )[0]

    def put_room(self, identifier: str, room_put: RoomPut):
        """
        Attempts to assign the state of a room
        """

        self._session.put_resource(
            endpoint=f"/clip/v2/resource/room/{identifier}",
            obj=room_put,
            error_message=f"An error occurred trying to update the room with id {identifier}.",
        )
