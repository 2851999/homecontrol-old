from homecontrol.database.mysql.config import DatabaseConfig
from homecontrol.database.mysql.connection import DatabaseConnection


class DatabaseClient:
    """
    Handles the creation of connections to databases using the database config
    """

    config: DatabaseConfig

    def __init__(self) -> None:
        self.config = DatabaseConfig()

    def connect(self, database: str) -> DatabaseConnection:
        # Start a connection with the database
        return DatabaseConnection(self.config.get_connection_info(database))
