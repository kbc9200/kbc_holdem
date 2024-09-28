from enum import Enum


class UserPositionType(Enum):
    SB = 'SB'
    BB = 'BB'
    UTG = 'UTG'
    MP1 = 'MP1'
    MP2 = 'MP2'
    MP3 = 'MP3'
    HJ = 'HJ'
    CO = 'CO'
    BTN = 'BTN'

    def __int__(self) -> int:
        return convert_int[self]


convert_int = {UserPositionType.SB: 0, UserPositionType.BB: 1, UserPositionType.UTG: 2, UserPositionType.MP1: 3,
               UserPositionType.MP2: 4, UserPositionType.MP3: 5, UserPositionType.HJ: 6, UserPositionType.CO: 7, UserPositionType.BTN: 8}
