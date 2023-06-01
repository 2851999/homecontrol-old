from typing import Dict, List

import broadlink

from homecontrol.broadlink.config import BroadlinkConfig
from homecontrol.broadlink.device import BroadlinkDevice
from homecontrol.broadlink.structs import BroadlinkConnectionInfo
from homecontrol.exceptions import DeviceNotRegisteredError


class BroadlinkManager:
    """
    Handles a set of broadlink devices
    """

    _config: BroadlinkConfig
    _loaded_devices: Dict[str, BroadlinkDevice] = {}

    def __init__(self) -> None:
        self._config = BroadlinkConfig()

        # Load all registered devices immediately
        self.load_devices()

    def list_devices(self) -> List[str]:
        """
        Returns a list of loaded devices
        """
        return list(self._loaded_devices.keys())

    def register_device(self, name: str, ip_address: str):
        """
        Attempts to register a device

        Raises:
            broadlink.exceptions.NetworkTimeoutError: When there is a
                                connection issue
        """
        # TODO: Check it can connect before saving to config
        self._config.register_device(
            BroadlinkConnectionInfo(name=name, ip_address=ip_address)
        )
        self._config.save()

        self._load_device(name)

    def _load_device(self, name: str) -> broadlink.Device:
        """
        Loads a device from the config

        Raises:
            DeviceNotRegisteredError: If the device has not been registered
        """
        if not self._config.has_device(name):
            raise DeviceNotRegisteredError(
                f"The broadlink device with name '{name}' has not been registered"
            )
        connection_info = self._config.get_device(name=name)
        device = BroadlinkDevice(connection_info=connection_info)
        self._loaded_devices.update({name: device})

    def load_devices(self):
        """
        Loads all registered devices from config
        """
        if self._config.has_devices():
            devices = self._config.get_devices()

            # Load the devices
            for name in devices.keys():
                self._load_device(name)

    def get_device(self, name: str) -> BroadlinkDevice:
        """
        Returns a loaded broadlink device
        """
        if name in self._loaded_devices:
            return self._loaded_devices[name]
        raise DeviceNotRegisteredError(f"Device '{name}' is not registered")

    def record_ir_command(self, device_name: str, command_name: str):
        """
        Records and saves an IR command for a particular device
        """
        device = self.get_device(device_name)
        packet = device.get_ir_packet()
        self._config.register_ir_command(command_name, packet)
        self._config.save()

    def playback_ir_command(self, device_name: str, command_name: str):
        """
        Play's back a saved IR command for a particular device
        """
        device = self.get_device(device_name)
        packet = self._config.get_ir_command(command_name)
        device.send_ir_packet(packet)
