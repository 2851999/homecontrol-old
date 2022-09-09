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
            # Sometimes values are returned when with emtpy values and are not specefied
            # in the API, so ignore them here
            # Note: This may cause things to go missing if structure is not correct
            if key in types:
                current_type = types[key]
                if get_origin(current_type) == list:
                    list_type = get_args(current_type)[0]
                    setattr(self, key, dicts_to_list(list_type, dictionary[key]))
                else:
                    # Don't bother if value non-existent
                    if value is not None:
                        setattr(self, key, current_type(value))


class ResourceIdentifierGet(HueAPIObject):
    """
    Object for the Hue API
    """

    rid: str
    rtype: str


class Metadata(HueAPIObject):
    """
    Object for the Hue API
    """

    archetype: str
    name: str


class RoomGet(HueAPIObject):
    """
    Object for the Hue API
    """

    type: str
    id: str
    id_v1: str
    metadata: Metadata
    services: List[ResourceIdentifierGet]
    children: List[ResourceIdentifierGet]


class SceneImage(HueAPIObject):
    """
    Object for the Hue API
    """

    rid: str
    rtype: str


class SceneGetMetadata(HueAPIObject):
    """
    Object for the Hue API
    """

    name: str
    image: SceneImage


class SceneGroup(HueAPIObject):
    """
    Object for the Hue API
    """

    rid: str
    rtype: str


class ActionTarget(HueAPIObject):
    """
    Object for the Hue API
    """

    rid: str
    rtype: str


class On(HueAPIObject):
    """
    Object for the Hue API
    """

    on: bool


class Dimming(HueAPIObject):
    """
    Object for the Hue API
    """

    brightness: int


class ColorXY(HueAPIObject):
    """
    Object for the Hue API
    """

    x: float
    y: float


class Color(HueAPIObject):
    """
    Object for the Hue API
    """

    xy: ColorXY


class ColorTemperature(HueAPIObject):
    """
    Object for the Hue API
    """

    mirek: int


class GradientPointGet(HueAPIObject):
    """
    Object for the Hue API
    """

    color: Color


class Gradient(HueAPIObject):
    """
    Object for the Hue API
    """

    points: List[GradientPointGet]


class Effects(HueAPIObject):
    """
    Object for the Hue API
    """

    effect: str


class Dynamics(HueAPIObject):
    """
    Object for the Hue API
    """

    duration: int


class Action(HueAPIObject):
    """
    Object for the Hue API
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
    Object for the Hue API
    """

    rid: str
    rtype: str


class ActionGet(HueAPIObject):
    """
    Object for the Hue API
    """

    target: Target
    action: Action


class ColorPaletteGet(HueAPIObject):
    """
    Object for the Hue API
    """

    color: Color
    dimming: Dimming


class DimmingFeatureBasicGet(HueAPIObject):
    """
    Object for the Hue API
    """

    brightness: int


class ColorTemperaturePaletteGet(HueAPIObject):
    """
    Object for the Hue API
    """

    color_temperature: ColorTemperature
    dimming: Dimming


class Palette(HueAPIObject):
    """
    Object for the Hue API
    """

    color: List[ColorPaletteGet]
    dimming: List[DimmingFeatureBasicGet]
    color_temperature: List[ColorTemperaturePaletteGet]


class SceneGet(HueAPIObject):
    """
    Object for the Hue API
    """

    type: str
    id: str
    id_v1: str
    metadata: SceneGetMetadata
    group: SceneGroup
    actions: List[ActionGet]
    palette: Palette
    speed: float
    auto_dynamic: bool


# class AlertEffectType(HueAPIObject):
#     """
#     Object for the Hue API
#     """


class Alert(HueAPIObject):
    """
    Object for the Hue API
    """

    action_values: List[str]


class GroupedLightGet(HueAPIObject):
    """
    Object for the Hue API
    """

    type: str
    id: str
    id_v1: str
    on: On
    alert: Alert


class DimmingDelta(HueAPIObject):
    """
    Object for the Hue API
    """

    action: str
    brightness_delta: int


class ColorTemperatureDelta(HueAPIObject):
    """
    Object for the Hue API
    """

    action: str
    mirek_delta: int


class GroupedLightPut(HueAPIObject):
    """
    Object for the Hue API
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


class ScenePutMetadata(HueAPIObject):
    """
    Object for the Hue API
    """

    name: str


class ActionPut(HueAPIObject):
    """
    Object for the Hue API
    """

    target: Target
    action: Action


class Recall(HueAPIObject):
    """
    Object for the Hue API
    """

    action: str
    status: str
    duration: str
    dimming: Dimming


class ScenePut(HueAPIObject):
    """
    Object for the Hue API
    """

    type: str
    metadata: ScenePutMetadata
    actions: List[ActionPut]
    recall: Recall
    palette: Palette
    speed: float


class Owner(HueAPIObject):
    """
    Object for the Hue API
    """

    rid: str
    rtype: str


class LightGetDimming(HueAPIObject):
    """
    Object for the Hue API
    """

    brightness: int
    min_dim_level: int


class MirekSchema(HueAPIObject):
    """
    Object for the Hue API
    """

    mirek_minimum: int
    mirek_maximum: int


class LightGetColorTemperature(HueAPIObject):
    """
    Object for the Hue API
    """

    mirek: int
    mirek_valid: bool
    mirek_schema: MirekSchema


class Gamut(HueAPIObject):
    """
    Object for the Hue API
    """

    red: ColorXY
    green: ColorXY
    blue: ColorXY


class LightGetColor(HueAPIObject):
    """
    Object for the Hue API
    """

    xy: ColorXY
    gamut: Gamut
    gamut_type: str


# class SupportedDynamicStatus(HueAPIObject):
#     """
#     Object for the Hue API
#     """


class LightGetDynamics(HueAPIObject):
    """
    Object for the Hue API
    """

    status: str
    status_values: List[str]
    speed: float
    speed_valid: bool


class LightGetGradient(Gradient):
    """
    Object for the Hue API
    """

    points_capable: int


# class SupportedEffects(HueAPIObject):
#     """
#     Object for the Hue API
#     """


class LightGetEffects(HueAPIObject):
    """
    Object for the Hue API
    """

    effect: str
    status_values: List[str]
    status: str
    effect_values: List[str]


class LightGetTimedEffects(HueAPIObject):
    """
    Object for the Hue API
    """

    effect: str
    duration: int
    status_values: List[str]
    status: str
    effect_values: List[str]


class LightGet(HueAPIObject):
    """
    Object for the Hue API
    """

    type: str
    id: str
    id_v1: str
    owner: Owner
    metadata: Metadata
    on: On
    dimming: LightGetDimming
    color_temperature: LightGetColorTemperature
    color: LightGetColor
    dynamics: LightGetDynamics
    alert: Alert
    mode: str
    gradient: LightGetGradient
    effects: LightGetEffects
    timed_effects: LightGetTimedEffects


class LightPutDynamics(HueAPIObject):
    """
    Object for the Hue API
    """

    duration: int
    speed: int


class LightPutAlert(HueAPIObject):
    """
    Object for the Hue API
    """

    action: str


class LightPutTimedEffects(HueAPIObject):
    """
    Object for the Hue API
    """

    effect: str
    duration: int


class LightPut(HueAPIObject):
    """
    Object for the Hue API
    """

    type: str
    # metadata: Metadata  # Depreciated
    on: On
    dimming: Dimming
    dimming_delta: DimmingDelta
    color_temperature: ColorTemperature
    color_temperature_delta: ColorTemperatureDelta
    color: Color
    dynamics: LightPutDynamics
    alert: LightPutAlert
    gradient: Gradient
    effects: Effects
    timed_effect: LightPutTimedEffects


class RoomPut(HueAPIObject):
    """
    Object for the Hue API
    """

    type: str
    metadata: Metadata
    children: List[ResourceIdentifierGet]
