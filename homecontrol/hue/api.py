from typing import Dict, List, get_args, get_origin, get_type_hints

from homecontrol.hue.helpers import dicts_to_list


class HueAPIObject:
    """
    Useful for creating class structures for the responses from
    the Hue API
    """

    def __init__(self, dictionary: Dict):
        types = get_type_hints(self)
        for key, value in dictionary.items():
            current_type = types[key]
            if get_origin(current_type) == list:
                list_type = get_args(current_type)[0]
                setattr(self, key, dicts_to_list(list_type, dictionary[key]))
            else:
                setattr(self, key, current_type(value))


class ResourceIdentifierGet(HueAPIObject):
    """
    Object returned by the Hue API
    """

    rid: str
    rtype: str


class RoomMetadata(HueAPIObject):
    """
    Object returned by the Hue API
    """

    archetype: str
    name: str


class RoomGet(HueAPIObject):
    """
    Object returned by the Hue API
    """

    type: str
    id: str
    id_v1: str
    metadata: RoomMetadata
    services: List[ResourceIdentifierGet]
    children: List[ResourceIdentifierGet]


class SceneImage(HueAPIObject):
    """
    Object returned by the Hue API
    """

    rid: str
    rtype: str


class SceneMetadata(HueAPIObject):
    """
    Object returned by the Hue API
    """

    name: str
    image: SceneImage


class SceneGroup(HueAPIObject):
    """
    Object returned by the Hue API
    """

    rid: str
    rtype: str


class ActionTarget(HueAPIObject):
    """
    Object returned by the Hue API
    """

    rid: str
    rtype: str


class On(HueAPIObject):
    """
    Object returned by the Hue API
    """

    on: bool


class Dimming(HueAPIObject):
    """
    Object returned by the Hue API
    """

    brightness: int


class ColorXY(HueAPIObject):
    """
    Object returned by the Hue API
    """

    x: float
    y: float


class Color(HueAPIObject):
    """
    Object returned by the Hue API
    """

    xy: ColorXY


class ColorTemperature(HueAPIObject):
    """
    Object returned by the Hue API
    """

    mirek: int


class GradientPointGet(HueAPIObject):
    """
    Object returned by the Hue API
    """

    color: Color


class Gradient(HueAPIObject):
    """
    Object returned by the Hue API
    """

    points: List[GradientPointGet]


class Effects(HueAPIObject):
    """
    Object returned by the Hue API
    """

    effect: str


class Dynamics(HueAPIObject):
    """
    Object returned by the Hue API
    """

    duration: int


class Action(HueAPIObject):
    """
    Object returned by the Hue API
    """

    on: On
    dimming: Dimming
    color: Color
    color_temperature: ColorTemperature
    gradient: Gradient
    effects: Effects
    dynamics: Dynamics


class Target(HueAPIObject):
    """
    Object returned by the Hue API
    """

    rid: str
    rtype: str


class ActionGet(HueAPIObject):
    """
    Object returned by the Hue API
    """

    target: Target
    action: Action


class ColorPaletteGet(HueAPIObject):
    """
    Object returned by the Hue API
    """

    color: Color
    dimming: Dimming


class DimmingFeatureBasicGet(HueAPIObject):
    """
    Object returned by the Hue API
    """

    brightness: int


class ColorTemperaturePaletteGet(HueAPIObject):
    """
    Object returned by the Hue API
    """

    color_temperature: ColorTemperature
    dimming: Dimming


class Palette(HueAPIObject):
    """
    Object returned by the Hue API
    """

    color: List[ColorPaletteGet]
    dimming: List[DimmingFeatureBasicGet]
    color_temperature: List[ColorTemperaturePaletteGet]


class SceneGet(HueAPIObject):
    """
    Object returned by the Hue API
    """

    type: str
    id: str
    id_v1: str
    metadata: SceneMetadata
    group: SceneGroup
    actions: List[ActionGet]
    palette: Palette
    speed: float
    auto_dynamic: bool


class AlertEffectType(HueAPIObject):
    """
    Object returned by the Hue API
    """


class Alert(HueAPIObject):
    """
    Object returned by the Hue API
    """

    action_values: AlertEffectType


class GroupedLightGet(HueAPIObject):
    """
    Object returned by the Hue API
    """

    type: str
    id: str
    id_v1: str
    on: On
    alert: Alert


class DimmingDelta(HueAPIObject):
    """
    Object returned by the Hue API
    """

    action: str
    brightness_delta: int


class ColorTemperatureDelta(HueAPIObject):
    """
    Object returned by the Hue API
    """

    action: str
    mirek_delta: int


class GroupedLightPut(HueAPIObject):
    """
    Object returned by the Hue API
    """

    type: str
    on: On
    dimming: Dimming
    dimming_delta: DimmingDelta
    color_temperature: ColorTemperature
    color_temperature_delta: ColorTemperatureDelta
    color: Color
    alert: Alert
    dynamics: Dynamics
