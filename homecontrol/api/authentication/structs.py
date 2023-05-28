from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserGroup(str, Enum):
    default = "default"
    admin = "admin"


@dataclass
class User:
    """Stores information about a user"""

    username: str
    uuid: str
    group: UserGroup


@dataclass
class InternalUser:
    """Stores internal information about a user"""

    username: str
    uuid: str
    password_hash: str
    group: UserGroup

    def to_user(self) -> User:
        """Returns a User instance excluding internal info"""
        return User(username=self.username, uuid=self.uuid, group=self.group)


@dataclass
class TokenPayload:
    """Authentication payload to include in an access token"""

    client_id: str
    exp: datetime
