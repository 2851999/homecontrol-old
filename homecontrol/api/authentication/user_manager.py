from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

from homecontrol.api.authentication.encryption import (
    check_password,
    decode_jwt,
    encode_jwt,
    generate_hash,
)
from homecontrol.api.authentication.structs import TokenPayload, User
from homecontrol.api.config import APIConfig
from homecontrol.api.database.client import APIDatabaseClient
from homecontrol.api.structs import APIAuthConfig
from homecontrol.exceptions import ResourceNotFoundError


class UserManager:
    """Handles users"""

    _auth_config: APIAuthConfig
    _database_client: APIDatabaseClient

    def __init__(
        self, api_config: APIConfig, database_client: APIDatabaseClient
    ) -> None:
        self._auth_config = api_config.get_auth()
        self._database_client = database_client

    def add_user(self, username: str, password: str):
        """
        Adds a new user

        Raises:
            UsernameAlreadyExistsError: If a user with the given username
                                        already exists
        """

        user = User(
            username=username, uuid=str(uuid4()), password_hash=generate_hash(password)
        )

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

    def _get_token_payload(self, user: User) -> TokenPayload:
        return TokenPayload(
            client_id=user.uuid,
            exp=datetime.utcnow() + timedelta(seconds=self._auth_config.token_expiry),
        )

    def generate_access_token(self, user: User) -> str:
        """
        Generates an access token for the user and returns it
        """
        return encode_jwt(
            self._get_token_payload(user).__dict__, self._auth_config.token_key
        )

    def verify_access_token(self, access_token: str) -> User:
        """
        Verifies an access token is valid and returns the user info
        """
        token_payload = decode_jwt(access_token, self._auth_config.token_key)
        token_payload = TokenPayload(**token_payload)

        # Obtain the user
        with self._database_client.connect() as conn:
            user = conn.users.find_user_by_id(token_payload.client_id)
        return user
