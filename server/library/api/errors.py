class LoLSenpaiException(Exception):
    pass


class BAD_PARAMETER(LoLSenpaiException):
    pass


class UNKNOWN_API(LoLSenpaiException):
    pass


class RATE_LIMIT_EXCEEDED(LoLSenpaiException):
    pass


class SUMMONERS_NOT_FOUND(LoLSenpaiException):
    pass


class GAME_NOT_FOUND(LoLSenpaiException):
    pass


class GAME_NOT_RANKED(LoLSenpaiException):
    pass


class SERVER_ERROR(LoLSenpaiException):
    pass