from typing import List

from homecontrol.helpers import ResponseStatus
from homecontrol.hue.api.structs import GroupedLightGet, GroupedLightPut
from homecontrol.hue.exceptions import HueAPIError
from homecontrol.hue.helpers import (
    dicts_to_list,
    object_to_dict,
)
from homecontrol.hue.session import HueBridgeSession


class GroupedLight:
    """
    Handles Philips Hue Room endpoints
    """

    _session: HueBridgeSession

    def __init__(self, session: HueBridgeSession) -> None:
        self._session = session

    def get_groups(self) -> List[GroupedLightGet]:
        """
        Returns a list of grouped lights
        """
        response = self._session.get("/clip/v2/resource/grouped_light")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get a list of light groups. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        data = response.json()["data"]
        return dicts_to_list(GroupedLightGet, data)

    def get_group(self, identifier: str) -> GroupedLightGet:
        """
        Returns the current state of a group of lights
        """
        response = self._session.get(f"/clip/v2/resource/grouped_light/{identifier}")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get the state of the light group with id {identifier}. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        data = response.json()["data"]
        return dicts_to_list(GroupedLightGet, data)[0]

    def put_group(self, identifier: str, grouped_light_put: GroupedLightPut):
        """
        Attempts to assign the state of a group of lights
        """

        response = self._session.put(
            f"/clip/v2/resource/grouped_light/{identifier}",
            json=object_to_dict(grouped_light_put),
        )

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to change the state of the light group with id {identifier} "
                f"Status code: {response.status_code}. Content {response.content}."
            )
