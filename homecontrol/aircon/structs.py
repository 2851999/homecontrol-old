from dataclasses import dataclass
from enum import IntEnum
from msmart.device import air_conditioning


@dataclass
class ACConnectionInfo:
    """
    For storing information required to connect to a device
    """

    name: str  # Added for UI purposes
    ip_address: str
    port: int
    identifier: int
    key: str
    token: str


class ACMode(IntEnum):
    """
    Wrapper for air conditioning modes
    """

    AUTO = air_conditioning.operational_mode_enum.auto  # 1
    COOL = air_conditioning.operational_mode_enum.cool  # 2
    DRY = air_conditioning.operational_mode_enum.dry  # 3
    HEAT = air_conditioning.operational_mode_enum.heat  # 4
    FAN = air_conditioning.operational_mode_enum.fan_only  # 5


class ACFanSpeed(IntEnum):
    """
    Wrapper for air conditioning fan speeds
    """

    AUTO = air_conditioning.fan_speed_enum.Auto  # 102
    FULL = air_conditioning.fan_speed_enum.Full  # 100
    MEDIUM = air_conditioning.fan_speed_enum.Medium  # 80
    LOW = air_conditioning.fan_speed_enum.Low  # 40
    SILENT = air_conditioning.fan_speed_enum.Silent  # 20


class ACSwingMode(IntEnum):
    """
    Wrapper for air conditioning fan speeds
    """

    OFF = air_conditioning.swing_mode_enum.Off  # 0x0, 0
    VERTICAL = air_conditioning.swing_mode_enum.Vertical  # 0xC 12
    HORIZONTAL = air_conditioning.swing_mode_enum.Horizontal  # 0x3 3
    BOTH = air_conditioning.swing_mode_enum.Both  # 0xF 15


@dataclass
class ACState:
    """
    For storing the state of a device
    """

    power: bool
    prompt_tone: bool
    target: int
    mode: ACMode
    fan: ACFanSpeed
    swing: ACSwingMode
    eco: bool
    turbo: bool
    fahrenheit: bool
    indoor: float
    outdoor: float
