from dataclasses import dataclass
from typing import List, Optional


@dataclass
class APIAuthConfig:
    """
    Stores auth config for the API
    """

    required: bool
    key: str
    token_key: str
    token_expiry: int


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


@dataclass
class APIInfo:
    """
    Stores information about the homecontrol API itself
    """

    version: str


@dataclass
class RoomState:
    """
    Stores information about a room state
    """

    state_id: str
    name: str
    room_name: str
    icon: str
    ac_device_name: Optional[str]
    ac_state_id: Optional[str]
    hue_scene_id: Optional[str]
    broadlink_device_name: Optional[str]
    broadlink_actions: Optional[List[str]]
