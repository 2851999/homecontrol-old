from homecontrol.client.helpers import check_response
from homecontrol.client.session import APISession


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
        response = self._session.get("/login/check")
        check_response(
            response, "An error occurred while trying to check the user login"
        )
        return response.json()
