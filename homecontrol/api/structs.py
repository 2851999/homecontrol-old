from dataclasses import dataclass


@dataclass
class APIAuthInfo:
    """
    Stores auth config for the API
    """

    required: bool
    key: str
