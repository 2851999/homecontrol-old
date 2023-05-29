from typing import List

from homecontrol.hue.api.session import HueBridgeSession
from homecontrol.hue.api.structs import GroupedLightGet, GroupedLightPut


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
        return self._session.get_resource(
            endpoint="/clip/v2/resource/grouped_light",
            class_type=GroupedLightGet,
            error_message="An error occurred trying to get a list of light groups.",
        )

    def get_group(self, identifier: str) -> GroupedLightGet:
        """
        Returns the current state of a group of lights
        """
        return self._session.get_resource(
            endpoint=f"/clip/v2/resource/grouped_light/{identifier}",
            class_type=GroupedLightGet,
            error_message=f"An error occurred trying to get the state of the light group with id {identifier}.",
        )[0]

    def put_group(self, identifier: str, grouped_light_put: GroupedLightPut):
        """
        Attempts to assign the state of a group of lights
        """

        self._session.put_resource(
            endpoint=f"/clip/v2/resource/grouped_light/{identifier}",
            obj=grouped_light_put,
            error_message=f"An error occurred trying to change the state of the light group with id {identifier}.",
        )
