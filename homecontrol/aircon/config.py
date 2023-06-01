from typing import Dict

from homecontrol.aircon.structs import ACAccountConfig, ACConnectionInfo
from homecontrol.config import Config


class ACConfig(Config):
    """
    Handles the aircon.json config
    """

    def __init__(self) -> None:
        super().__init__("aircon.json")

    def get_account(self) -> ACAccountConfig:
        """
        Returns an ACAccountConfig instance from loaded config
        """
        return ACAccountConfig(**self.data["account"])

    def has_devices(self):
        """
        Returns whether the loaded config has any devices stored in it
        """
        return "devices" in self.data

    def get_devices(self) -> Dict[str, Dict]:
        """
        Returns the devices listed in config

        Does not check for existence first
        """
        return self.data["devices"]

    def has_device(self, name: str) -> bool:
        """
        Returns whether a device with a particular name has been registered
        """
        return self.has_devices() and (name in self.data["devices"])

    def get_device(self, name: str) -> ACConnectionInfo:
        """
        Returns an ACConnectionInfo instance from loaded config given the
        name of the device
        """
        device_data = self.data["devices"][name]
        return ACConnectionInfo(name=name, **device_data)

    def register_device(self, connection_info: ACConnectionInfo):
        """
        Registers a device by updating the config
        """
        devices = self.data["devices"] if self.has_devices() else {}

        # No need to store the name as it's in the key
        connection_info_data = connection_info.__dict__.copy()
        del connection_info_data["name"]

        devices.update({connection_info.name: connection_info_data})
        self.data.update({"devices": devices})
