from dataclasses import dataclass


@dataclass
class DatabaseConnectionInfo:
    """
    For storing information required to connect to a mysql database
    """

    database: str
    host: str
    username: str
    password: str
