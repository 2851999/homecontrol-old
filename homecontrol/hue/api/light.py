from typing import List

from homecontrol.helpers import ResponseStatus, dicts_to_list, object_to_dict
from homecontrol.hue.api.structs import LightGet, LightPut
from homecontrol.hue.exceptions import HueAPIError
from homecontrol.hue.session import HueBridgeSession


class Light:
    """
    Handles Philips Hue Room endpoints
    """

    _session: HueBridgeSession

    def __init__(self, session: HueBridgeSession) -> None:
        self._session = session

    def get_lights(self) -> List[LightGet]:
        """
        Returns the current state of a group of lights
        """

        return self._session.get_resource(
            endpoint="/clip/v2/resource/light",
            class_type=LightGet,
            error_message="An error occurred trying to get a list of lights.",
        )

    def get_light(self, identifier: str) -> LightGet:
        """
        Returns the current state of a group of lights
        """

        return self._session.get_resource(
            endpoint=f"/clip/v2/resource/light/{identifier}",
            class_type=LightGet,
            error_message=f"An error occurred trying to get the state of the light with id {identifier}.",
        )[0]

    def put_light(self, identifier: str, light_put: LightPut):
        """
        Attempts to assign the state of a light
        """

        self._session.put_resource(
            endpoint=f"/clip/v2/resource/light/{identifier}",
            obj=light_put,
            error_message=f"An error occurred trying to change the state of the light with id {identifier}.",
        )
