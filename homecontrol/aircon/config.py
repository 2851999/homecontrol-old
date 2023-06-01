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
        return ACConnectionInfo(
            name=name,
            ip_address=device_data["ip"],
            identifier=device_data["id"],
            port=device_data["port"],
            key=device_data["key"],
            token=device_data["token"],
        )

    def register_device(self, connection_info: ACConnectionInfo):
        """
        Registers a device by updating the config
        """
        devices = self.data["devices"] if self.has_devices() else {}
        devices.update(
            {
                connection_info.name: {
                    "ip": connection_info.ip_address,
                    "id": connection_info.identifier,
                    "port": connection_info.port,
                    "key": connection_info.key,
                    "token": connection_info.token,
                }
            }
        )
        self.data.update({"devices": devices})
