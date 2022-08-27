from typing import Dict, List

from homecontrol.aircon.aircon import ACDevice
from homecontrol.aircon.config import ACConfig
from homecontrol.aircon.structs import ACConnectionInfo
from homecontrol.exceptions import DeviceNotRegistered


class ACManager:
    """
    Handles a set of aircon units
    """

    config: ACConfig
    loaded_devices: Dict[str, ACDevice] = {}

    def __init__(self) -> None:
        self.config = ACConfig()

        # Load all registered devices immediately
        self.load_devices()

    def register_device(self, name: str, ip_address: str):
        """
        Attempts to register a device
        """
        result = ACDevice.discover(name=name, ip_address=ip_address)
        if result:
            self.config.register_device(result)
            self.config.save()

            self._load_device(name)

    def _load_device(self, name: str) -> ACDevice:
        """
        Loads a device from the config

        :raises: ACDeviceNotRegistered if the device has not been registered
        """
        if not self.config.has_device(name):
            raise DeviceNotRegistered(
                f"The device with name '{name}' has not been registered"
            )
        connection_info = self.config.get_device(name=name)
        device = ACDevice(connection_info)
        self.loaded_devices.update({name: device})

    def load_devices(self):
        """
        Loads all registered devices from config
        """
        if self.config.has_devices():
            devices = self.config.get_devices()

            # Load the devices
            for name in devices.keys():
                self._load_device(name)

    def get_device(self, name: str) -> ACDevice:
        """
        Retrurns a loaded ACDevice
        """
        if name in self.loaded_devices:
            return self.loaded_devices[name]
        raise DeviceNotRegistered("Device is not registered")
