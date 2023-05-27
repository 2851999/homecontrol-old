from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """Stores information about a user"""

    username: str
    uuid: str
    password_hash: str


@dataclass
class TokenPayload:
    """Authentication payload to include in an access token"""

    client_id: str
    exp: datetime
