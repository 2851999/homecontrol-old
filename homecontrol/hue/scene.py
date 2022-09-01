from typing import List

from homecontrol.hue.api.api import HueBridgeAPI
from homecontrol.hue.api.structs import ScenePut
from homecontrol.hue.structs import HueScene


class Scene:
    """
    Handles Philips Hue Scene endpoints
    """

    _api: HueBridgeAPI

    def __init__(self, api: HueBridgeAPI) -> None:
        self._api = api

    def get_scenes(self) -> List[HueScene]:
        """
        Returns a list of available scenes
        """
        scenes = self._api.scene.get_scenes()
        scene_list = []
        for scene in scenes:
            room = None

            if scene.group.rtype == "room":
                room = scene.group.rid

            scene_list.append(
                HueScene(
                    identifier=scene.id,
                    name=scene.metadata.name,
                    room=room,
                )
            )

        return scene_list

    def recall_scene(self, identifier: str):
        """
        Attempts to recall a scene
        """

        # TODO: Allow dynamic_palette instead of active
        payload = ScenePut({"recall": {"action": "active"}})
        self._api.scene.put_scene(identifier=identifier, scene_put=payload)
