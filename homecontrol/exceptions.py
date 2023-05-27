class DeviceNotRegisteredError(Exception):
    """
    Raised when attempting to get a device that hasn't been registered
    """


class ResourceNotFoundError(Exception):
    """
    Raised when a particular resource is not found
    """
