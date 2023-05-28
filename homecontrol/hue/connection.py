from typing import Optional

from homecontrol.hue.api.api import HueBridgeAPI
from homecontrol.hue.grouped_light import GroupedLight
from homecontrol.hue.light import Light
from homecontrol.hue.room import Room
from homecontrol.hue.scene import Scene
from homecontrol.hue.session import HueBridgeSession
from homecontrol.hue.structs import HueBridgeAuthConfig, HueBridgeConnectionConfig


class HueBridgeConnection:
    """
    Handles the connection to a hue bridge
    """

    session: HueBridgeSession

    api: HueBridgeAPI
    room: Room
    light: Light
    grouped_light: GroupedLight
    scene: Scene

    def __init__(
        self,
        connection_config: HueBridgeConnectionConfig,
        ca_cert: str,
        auth_config: Optional[HueBridgeAuthConfig] = None,
    ) -> None:
        """
        Args:
            connection_config (HueBridgeConnectionConfig):
                           HueBridgeConnectionConfig instance for the bridge
            ca_cert (str): Path to the CA certificate for authenticating with
                           the bridge
            auth_config (Optional[HueBridgeAuthConfig]): Authentication info
                           for the bridge (may be None if not registered yet)
        """
        self.session = HueBridgeSession(
            connection_config=connection_config,
            ca_cert=ca_cert,
            auth_config=auth_config,
        )

    def __enter__(self):
        self.session.start()
        self.api = HueBridgeAPI(self.session)
        self.room = Room(self.api)
        self.light = Light(self.api)
        self.grouped_light = GroupedLight(self.api)
        self.scene = Scene(self.api)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.session.close()
