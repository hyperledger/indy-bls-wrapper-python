from enum import IntEnum


class ErrorCode(IntEnum):
    Success = 0
    Fail = 1


class IndyBlsError(Exception):
    pass
