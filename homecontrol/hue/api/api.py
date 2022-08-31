from homecontrol.hue.api.room import Room
from homecontrol.hue.api.scene import Scene
from homecontrol.hue.api.grouped_light import GroupedLight
from homecontrol.hue.session import HueBridgeSession


class HueBridgeAPI:
    """
    Handles the API of a bridge
    """

    room: Room
    grouped_light: GroupedLight
    scene: Scene

    def __init__(self, session: HueBridgeSession) -> None:
        self._session = session
        self.room = Room(session)
        self.grouped_light = GroupedLight(session)
        self.scene = Scene(session)
