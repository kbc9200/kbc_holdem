from enum import Enum


class UserActionType(Enum):
    BLIND = 'Blind'
    WAIT = 'Wait'
    FOLD = 'Fold'
    CALL = 'Call'
    RAISE = 'Raise'
    CHECK = 'Check'
    ALL_IN = 'All In'
