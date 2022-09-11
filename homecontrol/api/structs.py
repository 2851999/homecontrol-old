from dataclasses import dataclass
from typing import Optional


@dataclass
class APIAuthInfo:
    """
    Stores auth config for the API
    """

    required: bool
    key: str


@dataclass
class Room:
    """
    Stores information about a room
    """

    name: str
    ac_device_name: Optional[str] = None
    hue_room_id: Optional[str] = None
    hue_light_group: Optional[str] = None
