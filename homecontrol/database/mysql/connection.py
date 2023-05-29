from typing import Any, List, Optional, Tuple
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

    def create_table(self, table: str, values: List[str]):
        """
        Creates a table (if it does not already exist)

        values in format like 'key1 int', 'key2 varchar(255)'
        """
        # https://www.w3schools.com/mysql/mysql_create_table.asp
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {table}({','.join(values)})")

    def insert_values(self, table: str, values: List[Tuple[Any]]):
        """
        Inserts values into a table
        """

        # Inserts values into a table
        placeholders = ",".join(["%s"] * len(values[0]))

        sql = f"INSERT INTO {table} VALUES({placeholders})"
        self._cursor.executemany(sql, values)

    def select_values(
        self,
        table: str,
        values: List[str],
        where: Optional[Tuple[str, Tuple[Any]]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ):
        """
        Returns values from a table

        'where' is taken as a string statement and any values that will be replacing
        %s's to avoid SQL injection
        """
        sql = f"SELECT {','.join(values)} FROM {table}"
        params = ()

        if where is not None:
            sql += f" WHERE {where[0]}"
            params += where[1]
        if order_by is not None:
            sql += f" ORDER BY %s"
            params += (order_by,)
        if limit is not None:
            sql += f" LIMIT %s"
            params += (limit,)

        self._cursor.execute(sql, params or None)
        return self._cursor.fetchall()

    def commit(self):
        """
        Commits changes
        """
        self._connection.commit()
