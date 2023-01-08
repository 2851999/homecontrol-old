from typing import List
from homecontrol.api.structs import Room
from homecontrol.client.exceptions import APIError
from homecontrol.helpers import ResponseStatus, dataclass_list_from_dict
from homecontrol.client.session import APISession


class Home:
    """
    Handles home endpoints
    """

    _session: APISession

    def __init__(self, session: APISession) -> None:
        self._session = session

    def list_rooms(self, hue_bridge: str) -> List[Room]:
        """
        Returns a list of rooms in the house
        """
        response = self._session.get("/home/rooms", params={"bridge_name": hue_bridge})
        if response.status_code != ResponseStatus.OK:
            raise APIError("An error occurred listing rooms in the house")
        return dataclass_list_from_dict(Room, response.json())

    def get_outdoor_temp(self) -> str:
        """
        Returns the outdoor temperature (or N/A if there are no AC units available)
        """
        response = self._session.get("/home/outdoor_temp")
        if response.status_code != ResponseStatus.OK:
            raise APIError("An error occurred obtaining the outdoor temperature")
        return response.json()
