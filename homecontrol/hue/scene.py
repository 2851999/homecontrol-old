import json
from typing import Dict, List
from homecontrol.helpers import ResponseStatus
from homecontrol.hue.exceptions import HueAPIError
from homecontrol.hue.session import HueBridgeSession
from homecontrol.hue.structs import HueRoom, HueScene


class Scene:
    """
    Handles Philips Hue Scene endpoints
    """

    _session: HueBridgeSession

    def __init__(self, session: HueBridgeSession) -> None:
        self._session = session

    def get_scenes(self) -> List[HueScene]:
        """
        Returns a list of available scenes
        """
        scenes = []
        response = self._session.get("/clip/v2/resource/scene")

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to get scenes. "
                f"Status code: {response.status_code}. Content {response.content}."
            )

        # Obtain the data
        data = response.json()["data"]

        for scene in data:
            room = None

            if scene["group"]["rtype"] == "room":
                room = scene["group"]["rid"]

            scenes.append(
                HueScene(
                    identifier=scene["id"], name=scene["metadata"]["name"], room=room
                )
            )

        return scenes

    def recall_scene(self, identifier: str):
        """
        Attempts to recall a scene
        """

        # TODO: Allow dynamic_palette instead of active
        payload = {"recall": {"action": "active"}}
        response = self._session.put(
            f"/clip/v2/resource/scene/{identifier}", json=payload
        )

        if response.status_code != ResponseStatus.OK:
            raise HueAPIError(
                f"An error occurred trying to recall a scene. "
                f"Status code: {response.status_code}. Content {response.content}."
            )
