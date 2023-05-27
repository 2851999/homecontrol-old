from homecontrol.api.authentication.user import User
from homecontrol.database.mysql.client import DatabaseClient
from homecontrol.database.mysql.connection import DatabaseConnection
from homecontrol.database.mysql.structs import DatabaseConnectionInfo


class HomeControlDatabaseConnection(DatabaseConnection):
    """
    Handles a connection to the homecontrol database
    """

    # Users table name
    TABLE_USERS = "users"

    def __init__(self, connection_info: DatabaseConnectionInfo) -> None:
        super().__init__(connection_info)

    def init_db(self):
        """
        Creates any necessary tables, for now just for Users
        """
        self.create_table(
            self.TABLE_USERS,
            [
                "username VARCHAR(255)",
                "uuid VARCHAR(255)",
                "password_hash VARCHAR(255)",
            ],
        )

    def add_user(self, user: User):
        """
        Adds a user to the database
        """
        self.insert_values(
            self.TABLE_USERS, [(user.username, user.uuid, user.password_hash)]
        )
        self.commit()

    def get_user_by_username(self, username: str):
        """
        Obtains a User object from the database given their username
        """
        user_data = self.select_values(
            self.TABLE_USERS,
            ["uuid", "password_hash"],
            where=(f"username=%s", (username,)),
            limit=1,
        )[0]
        return User(username=username, uuid=user_data[0], password_hash=user_data[1])


class HomeControlDatabaseClient(DatabaseClient):
    """
    Handles connection to the homecontrol database
    """

    def __init__(self) -> None:
        super().__init__()

    def connect(self) -> HomeControlDatabaseConnection:
        return HomeControlDatabaseConnection(
            self.config.get_connection_info("homecontrol")
        )
