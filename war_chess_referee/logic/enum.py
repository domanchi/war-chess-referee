from enum import Enum
from typing import TypeVar


class ResultType(Enum):
    VICTORY = 0
    BOTH_LOSE = 1
    ATTACKER_LOSE = 2
    DEFENDER_LOSE = 3

    PENDING = 4
    ERROR = 5


PieceType = TypeVar('Piece')


class Piece(Enum):
    FIELD_MARSHALL = 9
    GENERAL = 8
    LIEUTENANT_GENERAL = 7
    BRIGADIER = 6
    COLONEL = 5
    MAJOR = 4
    CAPTAIN = 3
    LIEUTENANT = 2
    ENGINEER = 1
    BOMB = 0
    MINE = -1
    FLAG = -2

    @classmethod
    def translate(cls, piece: str) -> PieceType:
        """
        :raises: KeyError
        """
        try:
            if piece[0] == '军':
                if piece[1] == '长':
                    return cls.GENERAL
                else:
                    return cls.FLAG
        except IndexError:
            raise KeyError

        mapping = {
            '司': cls.FIELD_MARSHALL,
            '师': cls.LIEUTENANT_GENERAL,
            '旅': cls.BRIGADIER,
            '团': cls.COLONEL,
            '营': cls.MAJOR,
            '连': cls.CAPTAIN,
            '排': cls.LIEUTENANT,
            '工': cls.ENGINEER,
            '炸': cls.BOMB,
            '地': cls.MINE,
        }

        return mapping[piece[0]]
