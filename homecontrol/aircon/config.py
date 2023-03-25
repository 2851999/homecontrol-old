from typing import Dict

from homecontrol.aircon.structs import ACAccountConfig, ACConnectionConfig
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
        account_data = self.data["account"]

        return ACAccountConfig(
            username=account_data["username"], password=account_data["password"]
        )

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

    def get_device(self, name: str) -> ACConnectionConfig:
        """
        Returns an ACConnectionConfig instance from loaded config given the
        name of the device
        """
        device_data = self.data["devices"][name]
        return ACConnectionConfig(
            name=name,
            ip_address=device_data["ip"],
            identifier=device_data["id"],
            port=device_data["port"],
            key=device_data["key"],
            token=device_data["token"],
        )

    def register_device(self, connection_config: ACConnectionConfig):
        """
        Registers a device by updating the config
        """
        devices = self.data["devices"] if self.has_devices() else {}
        devices.update(
            {
                connection_config.name: {
                    "ip": connection_config.ip_address,
                    "id": connection_config.identifier,
                    "port": connection_config.port,
                    "key": connection_config.key,
                    "token": connection_config.token,
                }
            }
        )
        self.data.update({"devices": devices})
