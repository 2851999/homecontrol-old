class DatabaseError(Exception):
    """
    Raised when something unexpected is found in the database
    """


class UsernameAlreadyExistsError(Exception):
    """
    Raised when attempting to add a user with a username that already exists
    """
