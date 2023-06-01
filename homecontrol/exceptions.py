class DeviceNotRegisteredError(Exception):
    """
    Raised when attempting to get a device that hasn't been registered
    """


class DeviceConnectionError(Exception):
    """
    Raised when the connection to some device fails
    """


class ResourceNotFoundError(Exception):
    """
    Raised when a particular resource is not found
    """
