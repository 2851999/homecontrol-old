from mysql import connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from homecontrol.database.mysql.structs import DatabaseConnectionInfo


class DatabaseConnection:
    """
    Handles a database connection to a mysql database
    """

    _connection_info: DatabaseConnectionInfo
    _connection: MySQLConnection
    _cursor: MySQLCursor

    def __init__(self, connection_info: DatabaseConnectionInfo) -> None:
        self._connection_info = connection_info

    def __enter__(self):
        self._connection = connector.connect(
            database=self._connection_info.database,
            username=self._connection_info.username,
            password=self._connection_info.password,
        )
        self._cursor = self._connection.cursor()

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._connection.close()
