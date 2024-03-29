import sys
from typing import Dict

from homecontrol.exceptions import DeviceNotRegisteredError
from homecontrol.hue.config import HueConfig
from homecontrol.hue.hue import HueBridge
from homecontrol.hue.structs import HueBridgeConnectionInfo


class HueManager:
    """
    Handles a set of hue bridges
    """

    _config: HueConfig
    _loaded_bridges: Dict[str, HueBridge] = {}

    def __init__(self) -> None:
        self._config = HueConfig()

        # Load all registered bridges immediately
        self.load_bridges()

    def register_bridge(self, name: str, connection_info: HueBridgeConnectionInfo):
        """
        Attempts to register a device if it hasn't been already
        """
        if not self._config.has_bridge(
            name
        ) or self._config.is_bridge_waiting_for_button(name):
            bridge = HueBridge(
                ca_cert=self._config.get_ca_cert(), connection_info=connection_info
            )

            with bridge.start_session() as conn:
                payload = {
                    "devicetype": "homecontrol#python_app",
                    "generateclientkey": True,
                }
                response = conn.session.post("/api", json=payload)

                if response.status_code == 200:
                    response_json = response.json()[0]

                    if ("error" in response_json) and (
                        response_json["error"]["type"] == 101
                    ):
                        # Waiting for link button to be pressed
                        self._config.add_bridge_waiting(
                            name=name, connection_info=connection_info
                        )
                        self._config.save()

                        # Waiting for link button to be pressed
                        sys.exit(
                            f"Press the link button on the bridge with ip "
                            f"{connection_info.ip_address} and run again"
                        )
                    elif "success" in response_json:
                        # Success
                        success = response_json["success"]

                        self._config.set_bridge_registered(
                            name=name,
                            username=success["username"],
                            clientkey=success["clientkey"],
                        )
                        self._config.save()

                        sys.exit(
                            f"Successfully registered bridge with ip {connection_info.ip_address}"
                        )

    def _load_bridge(self, name: str) -> HueBridge:
        """
        Loads a bridge from the config

        :raises: DeviceNotRegisteredError if the device has not been registered
        """
        if not self._config.has_bridge(name):
            raise DeviceNotRegisteredError(
                f"The device with name '{name}' has not been registered"
            )

        if not self._config.is_bridge_waiting_for_button(name):
            connection_info = self._config.get_bridge_connection_info(name=name)
            auth_config = self._config.get_bridge_auth_config(name=name)
            bridge = HueBridge(
                ca_cert=self._config.get_ca_cert(),
                connection_info=connection_info,
                connection_auth=auth_config,
            )
            self._loaded_bridges.update({name: bridge})

    def load_bridges(self):
        """
        Loads all registered devices from config
        """
        if self._config.has_bridges():
            bridges = self._config.get_bridges()

            # Load the devices
            for name in bridges.keys():
                self._load_bridge(name)

    def get_bridge(self, name: str) -> HueBridge:
        """
        Returns a loaded ACDevice
        """
        if name in self._loaded_bridges:
            return self._loaded_bridges[name]
        raise DeviceNotRegisteredError("Device is not registered")
