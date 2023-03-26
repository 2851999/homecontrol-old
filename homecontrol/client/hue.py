from typing import Dict, List, Optional
from homecontrol.client.exceptions import APIError
from homecontrol.client.helpers import get_url_search_params
from homecontrol.helpers import (
    ResponseStatus,
    dataclass_from_dict,
    dataclass_list_from_dict,
)
from homecontrol.client.session import APISession
from homecontrol.hue.grouped_light import GroupedLightState
from homecontrol.hue.structs import HueRoom, HueScene


class Hue:
    """
    Handles hue endpoints
    """

    _session: APISession

    def __init__(self, session: APISession) -> None:
        self._session = session

    def get_rooms(
        self, bridge_name: str, filters: Optional[Dict] = None
    ) -> List[HueRoom]:
        """
        Returns a dictionary of rooms handled by a bridge
        """
        response = self._session.get(
            f"/hue/{bridge_name}/rooms{get_url_search_params(filters)}"
        )
        if response.status_code != ResponseStatus.OK:
            raise APIError("An error occurred getting a list of rooms")

        rooms = []
        for room in response.json():
            rooms.append(dataclass_from_dict(HueRoom, room))

        return rooms

    def get_grouped_light_state(
        self, bridge_name: str, group_id: str
    ) -> Dict[str, HueRoom]:
        """
        Returns a the current state of a light group
        """
        response = self._session.get(f"/hue/{bridge_name}/grouped_lights/{group_id}")
        if response.status_code != ResponseStatus.OK:
            raise APIError("An error occurred getting a grouped light state")

        return GroupedLightState.from_dict(response.json())

    def set_grouped_light_state(
        self, bridge_name: str, group_id: str, state: GroupedLightState
    ) -> bool:
        """
        Assigns the state of a light group
        """
        response = self._session.put(
            f"/hue/{bridge_name}/grouped_lights/{group_id}", json=state.to_dict()
        )
        if response.status_code != ResponseStatus.OK:
            raise APIError("An error occurred assigning a grouped light state")

        return True

    def get_scenes(
        self, bridge_name: str, filters: Optional[Dict] = None
    ) -> List[HueScene]:
        """
        Returns a list of scenes
        """
        url = f"/hue/{bridge_name}/scenes{get_url_search_params(filters)}"

        response = self._session.get(url)
        if response.status_code != ResponseStatus.OK:
            raise APIError("An error occurred getting a list of rooms")

        return dataclass_list_from_dict(HueScene, response.json())

    def recall_scene(self, bridge_name: str, scene_id: str):
        """
        Returns a list of scenes
        """
        response = self._session.put(f"/hue/{bridge_name}/scenes/{scene_id}")
        if response.status_code != ResponseStatus.OK:
            raise APIError("An error occurred when recalling a scene")
