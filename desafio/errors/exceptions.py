class APIException(Exception):
    """All custom API Exceptions"""
    pass


class InvalidIDException(APIException):
    message="Invalid ID format"
    status=422


class ContentNotFoundException(APIException):
    message="Content not found"
    status=404