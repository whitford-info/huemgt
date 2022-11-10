from enum import Enum

__all__ = ["RequestMethodEnum"]

class RequestMethodEnum(str, Enum):
    """
    This is the enumerator for the request method used in various places. These are standard API request methods.
    """
    get = "get"
    post = "post"
    patch = "patch"
    update = "update"
    delete = "delete"
