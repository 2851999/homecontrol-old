from dataclasses import dataclass


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
