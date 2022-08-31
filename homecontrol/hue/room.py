from typing import List
from homecontrol.helpers import ResponseStatus
from homecontrol.hue.api import RoomGet
from homecontrol.hue.exceptions import HueAPIError
from homecontrol.hue.helpers import dicts_to_list
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
        Returns a dictionary of rooms where keys represent the room name
        and the values their id
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
