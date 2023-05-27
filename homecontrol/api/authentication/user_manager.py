from typing import Optional
from uuid import uuid4

from homecontrol.api.authentication.encryption import check_password, generate_hash
from homecontrol.api.authentication.user import User
from homecontrol.api.config import APIConfig
from homecontrol.api.database.client import APIDatabaseClient
from homecontrol.exceptions import ResourceNotFoundError


class UserManager:
    """Handles users"""

    _database_client: APIDatabaseClient

    def __init__(
        self, database_client: APIDatabaseClient
    ) -> None:
        self._database_client = database_client

    def add_user(self, username: str, password: str):
        """
        Adds a new user

        Raises:
            UsernameAlreadyExistsError: If a user with the given username
                                        already exists
        """
        
        user = User(username=username, uuid=str(uuid4()), password_hash=generate_hash(password))

        with self._database_client.connect() as conn:
            conn.users.add_user(user)

    def verify_login(self, username: str, password: str) -> Optional[User]:
        """
        Returns a user's info but only if the username and password are correct
        """
        # Find the user
        try:
            with self._database_client.connect() as conn:
                user = conn.users.find_user_by_username(username)
        except ResourceNotFoundError:
            return None
        # Compare hashes
        if check_password(password, user.password_hash):
            return user
        else:
            return None
