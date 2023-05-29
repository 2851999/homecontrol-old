from typing import List

from homecontrol.api.authentication.structs import User
from homecontrol.client.helpers import check_response
from homecontrol.client.session import APISession
from homecontrol.helpers import dataclass_from_dict, dataclass_list_from_dict


class Auth:
    """
    Handles authentication endpoints
    """

    _session: APISession

    def __init__(self, session: APISession) -> None:
        self._session = session

    def login(self, username: str, password: str):
        """
        Logs in as a particular user
        """
        response = self._session.post(
            "/login", json={"username": username, "password": password}
        )
        check_response(response, "Failed to login")
        self._session.set_access_token(response.json()["access_token"])

    def login_check(self):
        """Checks whether we are logged in"""
        response = self._session.get("/login")
        check_response(
            response, "An error occurred while trying to check the user login"
        )
        return dataclass_from_dict(User, response.json())

    def get_users(self) -> List[User]:
        """Returns a list of users (admin only)"""
        response = self._session.get("/auth/users")
        check_response(
            response, "An error occurred while trying to get a list of users"
        )
        return dataclass_list_from_dict(User, response.json())

    def get_user(self, user_id: str) -> User:
        """Returns a list of users (admin only)"""
        response = self._session.get(f"/auth/user/{user_id}")
        check_response(
            response,
            f"An error occurred while trying to get the user with id '{user_id}'",
        )
        return dataclass_from_dict(User, response.json())
