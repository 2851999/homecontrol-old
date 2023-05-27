from homecontrol.api.database.connection import APIDatabaseConnection
from homecontrol.database.mysql.client import DatabaseClient


class APIDatabaseClient(DatabaseClient):
    """
    Handles connection to the homecontrol database
    """

    def __init__(self) -> None:
        super().__init__()

    def connect(self) -> APIDatabaseConnection:
        return APIDatabaseConnection(self.config.get_connection_info("homecontrol"))
