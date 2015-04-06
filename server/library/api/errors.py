class LoLSenpaiException(Exception):
    pass


class BAD_PARAMETER(LoLSenpaiException):
    pass


class UNKNOWN_API(LoLSenpaiException):
    pass


class RATE_LIMIT_EXCEEDED(LoLSenpaiException):
    pass


class SERVER_ERROR(LoLSenpaiException):
    pass