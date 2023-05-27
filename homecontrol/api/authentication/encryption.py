import bcrypt
import jwt


def generate_hash(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def check_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def encode_jwt(payload: dict, key: str) -> str:
    return jwt.encode(payload, key, "HS256")


def decode_jwt(encoded_jwt: str, key: str) -> dict:
    return jwt.decode(encoded_jwt, key, ["HS256"])
