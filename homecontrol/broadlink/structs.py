from dataclasses import dataclass


@dataclass
class BroadlinkConnectionInfo:
    """
    For storing information required to connect to a device
    """

    name: str  # Added for UI purposes
    ip_address: str
