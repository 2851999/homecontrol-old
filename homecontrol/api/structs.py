from dataclasses import dataclass


@dataclass
class APIAuthInfo:
    """
    Stores auth config for the API
    """

    required: bool
    key: str


class ResponseStatus:
    """
    Various response codes
    """

    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
