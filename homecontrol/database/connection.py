import sqlite3


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

    def create_table(self, name: str, data: str):
        """
        Creates a table (if it does not already exist)

        data is in a format like 'timestamp TEXT, temp REAL'
        """
        # https://www.sqlite.org/datatype3.html#:~:text=2.2.-,Date%20and%20Time%20Datatype,DD%20HH%3AMM%3ASS.
        self._cursor.execute(f"CREATE TABLE IF NOT EXISTS {name}({data})")

    def commit(self):
        """
        Commits changes
        """
        self._conn.commit()
