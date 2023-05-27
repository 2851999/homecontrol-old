from typing import List, Optional

from homecontrol.aircon.structs import ACState
from homecontrol.api.helpers import authenticated_user
from homecontrol.client.exceptions import APIError
from homecontrol.client.session import APISession
from homecontrol.helpers import ResponseStatus, dataclass_from_dict


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
        if response.status_code != ResponseStatus.OK:
            raise APIError(response.json()["message"])
        self._session.set_access_token(response.json()["access_token"])

    def login_check(self):
        """Checks whether we are logged in"""
        response = self._session.get("/login/check")
        if response.status_code != ResponseStatus.OK:
            raise APIError(response.json()["message"])
        else:
            return response.json()
