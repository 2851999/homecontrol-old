from homecontrol.config import Config
from homecontrol.database.mysql.structs import DatabaseConnectionInfo


class DatabaseConfig(Config):
    """
    Handles the database.json config
    """

    def __init__(self) -> None:
        super().__init__("database.json")

    def get_connection_info(self, database: str) -> DatabaseConnectionInfo:
        """Returns connection info for a particular database"""

        database_connection_data = self.data[database]

        return DatabaseConnectionInfo(
            database=database,
            host=database_connection_data["host"],
            username=database_connection_data["username"],
            password=database_connection_data["password"],
        )
