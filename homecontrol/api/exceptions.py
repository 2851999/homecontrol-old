class APIError(Exception):
    """
    Error raised when there is an error within the homecontrol API
    """

    status_code: int
    message: str

    def __init__(self, message: str, status_code: int = 500) -> None:
        """
        Args:
            message (str): Error message
            status_code (int): Status code to return from the API if uncaught
        """

        super().__init__(message)
        self.status_code = status_code
        self.message = message
