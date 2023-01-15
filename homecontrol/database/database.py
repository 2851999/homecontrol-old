import re
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

    @staticmethod
    def clean_string(value):
        """
        Convert string into a valid variable name
        """
        # https://stackoverflow.com/questions/3303312/how-do-i-convert-a-string-to-a-valid-variable-name-in-python
        return re.sub(r"\W|^(?=\d)", "_", value)
