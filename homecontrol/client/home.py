from typing import List

from homecontrol.api.structs import Room, RoomState
from homecontrol.client.helpers import check_response
from homecontrol.client.session import APISession
from homecontrol.helpers import dataclass_from_dict, dataclass_list_from_dict


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
        check_response(response, "An error occurred listing rooms in the house")
        return dataclass_list_from_dict(Room, response.json())

    def get_outdoor_temp(self) -> str:
        """
        Returns the outdoor temperature (or N/A if there are no AC units available)
        """
        response = self._session.get("/home/outdoor_temp")
        check_response(response, "An error occurred obtaining the outdoor temperature")
        return response.json()

    def get_room_states(self, name: str):
        """
        Returns a list of room states for a given room
        """
        response = self._session.get(f"/home/room/{name}/states")
        check_response(
            response, f"An error occurred obtaining a list of room states for {name}"
        )
        return dataclass_list_from_dict(RoomState, response.json())

    def recall_room_state(self, state_id: str):
        """
        Recall a room state given it's ID
        """
        response = self._session.put(f"/home/rooms/state/{state_id}")
        check_response(
            response, f"An error occurred recalling the room state with id '{state_id}'"
        )
        return dataclass_from_dict(RoomState, response.json())
