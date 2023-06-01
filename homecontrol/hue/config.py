from homecontrol.config import Config
from homecontrol.hue.structs import HueBridgeAuthConfig, HueBridgeConnectionInfo


class HueConfig(Config):
    """
    Handles the hue.json config
    """

    def __init__(self) -> None:
        super().__init__("hue.json")

    def has_bridges(self) -> bool:
        """
        Returns true when the available bridges have been detected
        and saved into the config
        """
        return "bridges" in self.data

    def get_bridges(self):
        """
        Returns the bridges listed in config

        Does not check for existence first
        """
        return self.data["bridges"]

    def has_bridge(self, name: str) -> bool:
        """
        Returns whether a bridge with a particular name has been registered
        """
        return self.has_bridges() and (name in self.data["bridges"])

    def get_bridge(self, name: str):
        """
        Returns the config of a bridge

        Args:
            name (str): Bridge name
        """
        return self.data["bridges"][name]

    def is_bridge_waiting_for_button(self, name: str) -> bool:
        """
        Returns true if the given bridge is currently waiting for
        the user to press the button

        Args:
            name (str): Bridge to check
        """
        return "waiting" in self.data["bridges"][name]

    def add_bridge_waiting(self, name: str, connection_info: HueBridgeConnectionInfo):
        """
        Adds a bridge to the config in the waiting state
        """
        bridges_config = self.data["bridges"] if self.has_bridges() else {}

        bridges_config.update(
            {
                name: {
                    "waiting": True,
                    "identifier": connection_info.identifier,
                    "ip_address": connection_info.ip_address,
                    "port": connection_info.port,
                }
            }
        )
        self.data.update({"bridges": bridges_config})

    def set_bridge_registered(self, name: str, username: str, clientkey: str):
        """
        Updates a bridge's config after its button has been pressed

        Args:
            name (str): Name of bridge to update
            username (str): Username from the authentication response
            clientkey (str): Clientkey from the authentication response
        """

        # Overwrite any existing config (including the waiting value)
        bridge_config = self.get_bridge(name)
        bridge_config.update(
            {
                "username": username,
                "clientkey": clientkey,
            }
        )
        del bridge_config["waiting"]
        self.data["bridges"].update({name: bridge_config})

    def get_bridge_connection_info(self, name: str) -> HueBridgeConnectionInfo:
        """
        Returns HueBridgeAuthConfig given the bridge
        """
        bridge_info = self.get_bridge(name)
        return HueBridgeConnectionInfo(
            identifier=bridge_info["identifier"],
            ip_address=bridge_info["ip_address"],
            port=bridge_info["port"],
        )

    def get_bridge_auth_config(self, name: str) -> HueBridgeAuthConfig:
        """
        Returns HueBridgeAuthConfig given the bridge
        """
        bridge_info = self.get_bridge(name)
        return HueBridgeAuthConfig(
            username=bridge_info["username"], clientkey=bridge_info["clientkey"]
        )

    def get_ca_cert(self) -> str:
        """
        Returns the ca_cert parameter from the config
        """
        return self.data["ca_cert"]
