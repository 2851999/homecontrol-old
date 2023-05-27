from dataclasses import dataclass
from typing import Dict, Optional

from homecontrol.hue.api.api import HueBridgeAPI
from homecontrol.hue.api.structs import LightGet, LightPut
from homecontrol.hue.colour import HueColour
from homecontrol.hue.helpers import kelvin_to_mirek


@dataclass
class LightState:
    """
    Stores information about the state of a light,
    values are optional so only certain ones can be updated
    """

    name: str
    power: Optional[bool] = None
    brightness: Optional[int] = None
    colour: Optional[HueColour] = None
    colour_temp: Optional[int] = None

    @staticmethod
    def from_api(data: LightGet):
        """
        Returns an instance of this class from the dictionary obtained
        from the Hue API
        """

        return LightState(
            name=data.metadata.name,
            power=data.on.on,
            brightness=None,
            colour=None,
            colour_temp=None,
        )

    def to_update_payload(self) -> LightPut:
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
        return LightPut(payload)

    def to_dict(self) -> Dict:
        """
        Returns the dictionary representation of this object
        """

        return {
            "name": self.name,
            "power": self.power,
            "brightness": self.brightness,
            "colour": self.colour.__dict__ if self.colour is not None else None,
            "colour_temp": self.colour_temp,
        }

    @staticmethod
    def from_dict(dictionary):
        """
        Returns an instance of LightState from its dictionary representation
        """

        return LightState(
            name=dictionary["name"],
            power=dictionary["power"],
            brightness=dictionary["brightness"],
            colour=HueColour.from_dict(dictionary["colour"])
            if dictionary["colour"] is not None
            else None,
            colour_temp=dictionary["colour_temp"],
        )


class Light:
    """
    Handles Philips light endpoints
    """

    _api: HueBridgeAPI

    def __init__(self, api: HueBridgeAPI) -> None:
        self._api = api

    def get_state(self, identifier: str) -> LightGet:
        """
        Returns the current state of a group of lights
        """

        state = self._api.light.get_light(identifier=identifier)

        return LightState.from_api(state)

    def set_state(self, identifier: str, state: LightState):
        """
        Attempts to assign the state of a group of lights
        """

        self._api.light.put_light(
            identifier=identifier, light_put=state.to_update_payload()
        )
