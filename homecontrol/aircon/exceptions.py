class ACConnectionError(Exception):
    """
    Raised when fetching/updating some device state fails
    """


class ACInvalidStateError(Exception):
    """
    Raised when an invalid state is given
    """
