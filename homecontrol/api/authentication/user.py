from dataclasses import dataclass


@dataclass
class User:
    """Stores information about a user"""

    username: str
    uuid: str
    password_hash: str