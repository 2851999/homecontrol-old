from typing import List

from homecontrol.helpers import ResponseStatus, dicts_to_list, object_to_dict
from homecontrol.hue.api.structs import ScenePut
from homecontrol.hue.api.structs import SceneGet
from homecontrol.hue.exceptions import HueAPIError
from homecontrol.hue.session import HueBridgeSession


class Scene:
    """
    Handles Philips Hue Scene endpoints
    """

    _session: HueBridgeSession

    def __init__(self, session: HueBridgeSession) -> None:
        self._session = session

    def get_scenes(self) -> List[SceneGet]:
        """
        Returns a list of available scenes
        """

        return self._session.get_resource(
            endpoint="/clip/v2/resource/scene",
            class_type=SceneGet,
            error_message="An error occurred trying to get scenes."
        )

    def put_scene(self, identifier: str, scene_put: ScenePut):
        """
        Put request for a scene
        """

        self._session.put_resource(
            endpoint=f"/clip/v2/resource/scene/{identifier}",
            obj=scene_put,
            error_message=f"An error occurred trying to assign the state of the scene with id {identifier}."
        )
