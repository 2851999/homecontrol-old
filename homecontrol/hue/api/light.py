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
        response = self._session.get("/clip/v2/resource/light")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get a list of lights. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        data = response.json()["data"]
        return dicts_to_list(LightGet, data)

    def get_light(self, identifier: str) -> LightGet:
        """
        Returns the current state of a group of lights
        """
        response = self._session.get(f"/clip/v2/resource/light/{identifier}")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get a list of lights. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        data = response.json()["data"]
        return dicts_to_list(LightGet, data)[0]

    def put_light(self, identifier: str, light_put: LightPut):
        """
        Attempts to assign the state of a light
        """

        response = self._session.put(
            f"/clip/v2/resource/light/{identifier}",
            json=object_to_dict(light_put),
        )

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to change the state of the light with id {identifier} "
                f"Status code: {response.status_code}. Content {response.content}."
            )
