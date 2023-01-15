from homecontrol.database.connection import DatabaseConnection
from homecontrol.scheduling.structs import SchedulerDatabaseInfo


class Database:
    """
    Handles info for connecting to an sqlite3 database
    """

    # Path of this database
    config: SchedulerDatabaseInfo

    def __init__(self, config: SchedulerDatabaseInfo):
        self.config = config

    def start_session(self) -> DatabaseConnection:
        """
        Returns an DatabaseConnection instance for contacting a database
        e.g. 'with database.start_session() as session'
        """
        return DatabaseConnection(self.config.path)
