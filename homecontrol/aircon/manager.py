from typing import Dict, List

from homecontrol.aircon.aircon import ACDevice
from homecontrol.aircon.config import ACConfig
from homecontrol.exceptions import DeviceNotRegisteredError


class ACManager:
    """
    Handles a set of aircon devices
    """

    _config: ACConfig
    _loaded_devices: Dict[str, ACDevice] = {}

    def __init__(self) -> None:
        self._config = ACConfig()

        # Load all registered devices immediately
        self._load_devices()

    def list_devices(self) -> List[str]:
        """
        Returns a list of loaded devices
        """
        return list(self._loaded_devices.keys())

    def register_device(self, name: str, ip_address: str):
        """
        Attempts to register a device

        Raises:
            DeviceConnectionError: When there is a connection issue
        """
        result = ACDevice.discover(
            name=name, ip_address=ip_address, account_config=self._config.get_account()
        )
        if result:
            self._config.register_device(result)
            self._config.save()

            self._load_device(name)

    def _load_device(self, name: str) -> ACDevice:
        """
        Loads a device from the config

        Raises
            DeviceNotRegisteredError: If the device has not been registered
        """
        if not self._config.has_device(name):
            raise DeviceNotRegisteredError(
                f"Aircon device with name '{name}' has not been registered"
            )
        connection_info = self._config.get_device(name=name)
        device = ACDevice(connection_info)
        self._loaded_devices.update({name: device})

    def _load_devices(self):
        """
        Loads all registered devices from config
        """
        if self._config.has_devices():
            devices = self._config.get_devices()

            # Load the devices
            for name in devices.keys():
                self._load_device(name)

    def get_device(self, name: str) -> ACDevice:
        """
        Returns a loaded ACDevice
        """
        if name in self._loaded_devices:
            return self._loaded_devices[name]
        raise DeviceNotRegisteredError(f"Aircon device '{name}' is not registered")
