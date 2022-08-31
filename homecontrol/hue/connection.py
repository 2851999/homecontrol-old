from typing import Optional
from homecontrol.hue.api.api import HueBridgeAPI
from homecontrol.hue.grouped_light import GroupedLight
from homecontrol.hue.room import Room
from homecontrol.hue.scene import Scene

from homecontrol.hue.structs import HueBridgeAuthInfo, HueBridgeConnectionInfo
from homecontrol.hue.session import HueBridgeSession


class HueBridgeConnection:
    """
    Handles the connection to a hue bridge
    """

    session: HueBridgeSession

    api: HueBridgeAPI
    room: Room
    grouped_light: GroupedLight
    scene: Scene

    def __init__(
        self,
        connection_info: HueBridgeConnectionInfo,
        ca_cert: str,
        auth_info: Optional[HueBridgeAuthInfo] = None,
    ) -> None:
        """
        :param connection_info: HueBridgeConnectionInfo instance for the bridge
        :param ca_cert: Path to the CA certificate for authenticating with the bridge
        :param auth_info: Authentication info for the bridge (may be None if not registered yet)
        """
        self.session = HueBridgeSession(
            connection_info=connection_info, ca_cert=ca_cert, auth_info=auth_info
        )

    def __enter__(self):
        self.session.start()
        self.api = HueBridgeAPI(self.session)
        self.room = Room(self.api)
        self.grouped_light = GroupedLight(self.api)
        self.scene = Scene(self.api)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.session.close()
