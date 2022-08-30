from dataclasses import dataclass
from typing import List, Optional

from homecontrol.helpers import SubscriptableClass


@dataclass
class HueBridgeConnectionInfo:
    """
    For storing information required to connect to a hue bridge
    """

    identifier: str
    ip_address: str
    port: int


@dataclass
class HueBridgeAuthInfo:
    """
    For storing information required to authenticate a connection to a hue bridge
    """

    username: str
    clientkey: str


@dataclass
class HueRoom(SubscriptableClass):
    """
    For storing information about a room
    """

    identifier: str
    light_group: Optional[str]
    devices: List[str]


@dataclass
class HueScene(SubscriptableClass):
    """
    For storing information about a scene
    """

    identifier: str
    name: str
    room: Optional[str]
