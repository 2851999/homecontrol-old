from typing import Dict

from homecontrol.broadlink.structs import BroadlinkConnectionInfo
from homecontrol.config import Config


class BroadlinkConfig(Config):
    """
    Handles the aircon.json config
    """

    def __init__(self) -> None:
        super().__init__("broadlink.json")

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

    def get_device(self, name: str) -> BroadlinkConnectionInfo:
        """
        Returns an ACConnectionInfo instance from loaded config given the
        name of the device
        """
        device_data = self.data["devices"][name]
        return BroadlinkConnectionInfo(name=name, **device_data)

    def register_device(self, connection_info: BroadlinkConnectionInfo):
        """
        Registers a device by updating the config
        """

        # No need to store the name as it's in the key
        connection_info_data = connection_info.__dict__.copy()
        del connection_info_data["name"]

        devices = self.data["devices"] if self.has_devices() else {}
        devices.update(
            {
                connection_info.name: {
                    **connection_info_data,
                }
            }
        )
        self.data.update({"devices": devices})

    def register_ir_command(self, name: str, packet: bytes):
        """
        Registers an IR command by updating the config
        """
        commands = self.data["commands"] if "commands" in self.data else {}
        commands.update({name: packet.decode("latin1")})
        self.data.update({"commands": commands})

    def get_ir_command(self, name: str):
        """
        Registers an IR command loaded from the config
        """
        return self.data["commands"][name].encode("latin1")
