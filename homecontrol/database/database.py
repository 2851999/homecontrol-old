from homecontrol.database.connection import DatabaseConnection
from homecontrol.scheduling.structs import SchedulerDatabaseConfig


class Database:
    """
    Handles info for connecting to an sqlite3 database
    """

    # Config for this database
    config: SchedulerDatabaseConfig

    def __init__(self, config: SchedulerDatabaseConfig):
        self.config = config

    def start_session(self) -> DatabaseConnection:
        """
        Returns an DatabaseConnection instance for contacting a database
        e.g. 'with database.start_session() as session'
        """
        return DatabaseConnection(self.config.path)
