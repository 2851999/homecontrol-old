from dataclasses import dataclass
from typing import List, Optional


@dataclass
class APIAuthConfig:
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
    hue_lights: Optional[List[str]] = None
