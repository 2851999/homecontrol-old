from dataclasses import dataclass
from typing import Dict, Optional
from homecontrol.helpers import ResponseStatus
from homecontrol.hue.color import HueColour
from homecontrol.hue.exceptions import HueAPIError
from homecontrol.hue.helpers import kelvin_to_mirek, mirek_to_kelvin
from homecontrol.hue.session import HueBridgeSession


@dataclass
class GroupedLightState:
    """
    Stores information about the state of a light group,
    values are optional so only certain ones can be updated
    """

    power: Optional[bool] = None
    brightness: Optional[int] = None
    colour: Optional[HueColour] = None
    colour_temp: Optional[int] = None

    @staticmethod
    def from_dict(data: Dict):
        """
        Returns an instance of this class from the dictionary obtained
        from the Hue API
        """
        power = data["on"]["on"]
        brightness = data["dimming"]["brightness"]
        colour = None
        colour_temp = None

        if "xy" in data["color"]:
            colour = HueColour.from_dict(data["color"])

        if "mirek" in data["color_temperature"]:
            colour_temp = mirek_to_kelvin(data["color_temperature"]["mirek"])

        return GroupedLightState(
            power=power,
            brightness=brightness,
            colour=colour,
            colour_temp=colour_temp,
        )

    def to_update_payload(self) -> Dict:
        """
        Returns a payload for updating this light state
        """
        payload = {}
        if self.power is not None:
            payload.update({"on": {"on": self.power}})
        if self.brightness is not None:
            payload.update({"dimming": {"brightness": self.brightness}})
        if self.colour is not None:
            payload.update({"color": {"xy": self.colour.__dict__}})
        if self.colour_temp is not None:
            payload.update(
                {"color_temperature": {"mirek": kelvin_to_mirek(self.colour_temp)}}
            )
        return payload


class GroupedLight:
    """
    Handles Philips Hue Room endpoints
    """

    _session: HueBridgeSession

    def __init__(self, session: HueBridgeSession) -> None:
        self._session = session

    def get_state(self, identifier: str) -> GroupedLightState:
        """
        Returns the current state of a group of lights
        """
        response = self._session.get(f"/clip/v2/resource/grouped_light/{identifier}")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to change the power state of a room. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        data = response.json()["data"][0]
        return GroupedLightState.from_dict(data)

    def set_state(self, identifier: str, state: GroupedLightState):
        """
        Attempts to assign the state of a group of lights
        """

        response = self._session.put(
            f"/clip/v2/resource/grouped_light/{identifier}",
            json=state.to_update_payload(),
        )

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to change the lighting state of a room. "
                f"Status code: {response.status_code}. Content {response.content}."
            )
