import bcrypt

def generate_hash(password: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def check_password(password: str, password_hash: str):
    return bcrypt.checkpw(password.encode(), password_hash.encode())