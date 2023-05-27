from homecontrol.hue.api.device import Device
from homecontrol.hue.api.grouped_light import GroupedLight
from homecontrol.hue.api.light import Light
from homecontrol.hue.api.room import Room
from homecontrol.hue.api.scene import Scene
from homecontrol.hue.session import HueBridgeSession


class HueBridgeAPI:
    """
    Handles the API of a bridge
    """

    light: Light
    room: Room
    grouped_light: GroupedLight
    scene: Scene
    device: Device

    def __init__(self, session: HueBridgeSession) -> None:
        self._session = session
        self.light = Light(session)
        self.room = Room(session)
        self.grouped_light = GroupedLight(session)
        self.scene = Scene(session)
        self.device = Device(session)
