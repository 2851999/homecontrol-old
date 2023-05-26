import sqlite3
from typing import Any, List, Optional, Tuple


class DatabaseConnection:
    """
    Handles a connection to a sqlite3 database
    """

    # Path of this database
    path: str

    # Connection
    _conn: sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self, path: str):
        self.path = path

    def __enter__(self):
        self._conn = sqlite3.connect(self.path)
        self._cursor = self._conn.cursor()

        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._conn.close()

    def join_with(self, join_str: str, values: List[str]) -> str:
        # Joins a list of strings with a given value ignoring the last
        return join_str.join(values)

    def create_table(self, table: str, values: List[str]):
        """
        Creates a table (if it does not already exist)

        values in format like 'timestamp TEXT', 'temp REAL'
        """
        # https://www.sqlite.org/datatype3.html#:~:text=2.2.-,Date%20and%20Time%20Datatype,DD%20HH%3AMM%3ASS.
        self._cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table}({self.join_with(',', values)})"
        )

    def insert_values(self, table: str, values: List[Tuple[Any]]):
        """
        Inserts values into a table
        """

        # Inserts values into a table
        placeholders = self.join_with(",", ["?"] * len(values[0]))

        sql = f"INSERT INTO {table} VALUES({placeholders})"
        self._cursor.executemany(sql, values)

    def select_values(
        self,
        table: str,
        values: List[str],
        where: Optional[str] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ):
        """
        Returns values from a table
        """
        sql = f"SELECT {self.join_with(',', values)} FROM {table}"

        if where is not None:
            sql += f" WHERE {where}"
        if order_by is not None:
            sql += f" ORDER BY {order_by}"
        if limit is not None:
            sql += f" LIMIT {limit}"

        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def commit(self):
        """
        Commits changes
        """
        self._conn.commit()
