from typing import Optional
from homecontrol.hue.grouped_light import GroupedLight
from homecontrol.hue.room import Room

from homecontrol.hue.structs import HueBridgeAuthInfo, HueBridgeConnectionInfo
from homecontrol.hue.session import HueBridgeSession


class HueBridgeConnection:
    """
    Handles the connection to a hue bridge
    """

    session: HueBridgeSession

    room: Room
    grouped_light: GroupedLight

    def __init__(
        self,
        connection_info: HueBridgeConnectionInfo,
        ca_cert: str,
        auth_info: Optional[HueBridgeAuthInfo] = None,
    ) -> None:
        """
        :param connection_info: HueBridgeConnectionInfo instance for the bridge
        :param ca_cert: Path to the CA certificate for authenticating with the bridge
        """
        self.session = HueBridgeSession(
            connection_info=connection_info, ca_cert=ca_cert, auth_info=auth_info
        )

    def __enter__(self):
        self.session.start()
        self.room = Room(self.session)
        self.grouped_light = GroupedLight(self.session)

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.session.close()
