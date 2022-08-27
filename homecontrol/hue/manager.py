import sys
from typing import Dict
from homecontrol.exceptions import DeviceNotRegistered
from homecontrol.hue.bridge_structs import HueBridgeConnectionInfo
from homecontrol.hue.config import HueConfig
from homecontrol.hue.hue import HueBridge


class HueManager:
    """
    Handles a set of hue bridges
    """

    config: HueConfig
    loaded_bridges: Dict[str, HueBridge] = {}

    def __init__(self) -> None:
        self.config = HueConfig()

        # Load all registered devices immediately
        self.load_devices()

    def register_bridge(self, name: str, connection_info: HueBridgeConnectionInfo):
        """
        Attempts to register a device if it hasn't been already
        """
        if not self.config.has_bridge(name) or self.config.is_bridge_waiting_for_button(
            name
        ):
            bridge = HueBridge(
                ca_cert=self.config.get_ca_cert(), connection_info=connection_info
            )

            with bridge.start_session() as session:
                payload = {
                    "devicetype": "homecontrol#python_app",
                    "generateclientkey": True,
                }
                response = session.post("/api", json=payload)

                if response.status_code == 200:
                    response_json = response.json()[0]

                    if ("error" in response_json) and (
                        response_json["error"]["type"] == 101
                    ):
                        # Waiting for link button to be pressed
                        self.config.add_bridge_waiting(
                            name=name, connection_info=connection_info
                        )
                        self.config.save()

                        # Waiting for link button to be pressed
                        sys.exit(
                            f"Press the link button on the bridge with ip "
                            f"{connection_info.ip_address} and run again"
                        )
                    elif "success" in response_json:
                        # Success
                        success = response_json["success"]

                        self.config.set_bridge_registered(
                            name=name,
                            username=success["username"],
                            clientkey=success["clientkey"],
                        )
                        self.config.save()

                        sys.exit(
                            f"Successfully registered bridge with ip {connection_info.ip_address}"
                        )

    def _load_bridge(self, name: str) -> HueBridge:
        """
        Loads a bridge from the config

        :raises: DeviceNotRegistered if the device has not been registered
        """
        if not self.config.has_bridge(name):
            raise DeviceNotRegistered(
                f"The device with name '{name}' has not been registered"
            )

        if not self.config.is_bridge_waiting_for_button(name):
            connection_info = self.config.get_bridge(name=name)
            auth_info = self.config.get_bridge_auth_info(name=name)
            bridge = HueBridge(
                ca_cert=self.config.get_ca_cert(),
                connection_info=connection_info,
                connection_auth=auth_info,
            )
            self.loaded_bridges.update({name: bridge})

    def load_devices(self):
        """
        Loads all registered devices from config
        """
        if self.config.has_bridges():
            bridges = self.config.get_bridges()

            # Load the devices
            for name in bridges.keys():
                self._load_bridge(name)

    def get_bridge(self, name: str) -> HueBridge:
        """
        Retrurns a loaded ACDevice
        """
        if name in self.loaded_bridges:
            return self.loaded_bridges[name]
        raise DeviceNotRegistered("Device is not registered")
