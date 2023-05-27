from homecontrol.api.authentication.user import User
from homecontrol.api.database.exceptions import (
    DatabaseError,
    UsernameAlreadyExistsError,
)
from homecontrol.database.mysql.connection import DatabaseConnection
from homecontrol.exceptions import ResourceNotFoundError


class Users:
    """Handles users in the database"""

    # Users table name
    TABLE_USERS = "users"

    _connection: DatabaseConnection

    def __init__(self, connection: DatabaseConnection) -> None:
        self._connection = connection

    def create_table(self):
        """
        Creates the table required for storing users in the database
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

        Raises:
            UsernameAlreadyExistsError: If a user with the given username
                                        already exists
        """
        # Ensure the user doesn't already exist
        if self.does_user_exist(user.username):
            raise UsernameAlreadyExistsError(
                f"A user with the username '{user.username}' already exists"
            )

        self._connection.insert_values(
            self.TABLE_USERS, [(user.username, user.uuid, user.password_hash)]
        )
        self._connection.commit()

    def does_user_exist(self, username: str):
        """
        Returns whether a user with a particular username exists
        """
        try:
            self.get_user_by_username(username)
            return True
        except ResourceNotFoundError:
            return False

    def get_user_by_username(self, username: str):
        """
        Obtains a User object from the database given their username

        Raises:
            ResourceNotFoundError: If the user with the given username is not
                                   found
            DatabaseError: If for some reason more than one user has the given
                           username
        """
        user_data = self._connection.select_values(
            self.TABLE_USERS,
            ["uuid", "password_hash"],
            where=(f"username=%s", (username,)),
        )

        if len(user_data) == 0:
            raise ResourceNotFoundError(
                f"User with the username '{username}' could not be found in the database"
            )
        if len(user_data) > 1:
            raise DatabaseError(
                f"{len(user_data)} users were found to have the username '{username}' in the database"
            )
        user_data = user_data[0]
        return User(username=username, uuid=user_data[0], password_hash=user_data[1])
