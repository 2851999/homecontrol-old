from typing import List

from homecontrol.helpers import ResponseStatus
from homecontrol.hue.api.structs import ScenePut
from homecontrol.hue.api.structs import SceneGet
from homecontrol.hue.exceptions import HueAPIError
from homecontrol.hue.helpers import dicts_to_list, object_to_dict
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
        response = self._session.get("/clip/v2/resource/scene")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get scenes. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        # Obtain the data
        data = response.json()["data"]

        return dicts_to_list(SceneGet, data)

    def put(self, identifier: str, scene_put: ScenePut):
        """
        Put request for a scene
        """

        response = self._session.put(
            f"/clip/v2/resource/scene/{identifier}", json=object_to_dict(scene_put)
        )

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to assign a scene's state. "
                f"Status code: {response.status_code}. Content {response.content}."
            )
