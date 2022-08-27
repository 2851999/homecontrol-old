from dataclasses import dataclass


@dataclass
class APIConnectionInfo:
    """
    For storing information required to connect to the homecontrol api
    """

    auth_required: bool
    auth_key: str
    ip_address: str
    port: int
