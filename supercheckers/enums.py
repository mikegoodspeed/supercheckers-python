import enum


class PlayState(enum.Enum):
    NOT_STARTED = enum.auto()
    IN_PROGRESS = enum.auto()
    COMPLETE = enum.auto()
    ERROR = enum.auto()


class Team(enum.Enum):
    ONE = "X"
    TWO = "O"


class Direction(enum.Enum):
    UNKNOWN = enum.auto()
    NORTH = enum.auto()
    SOUTH = enum.auto()
    EAST = enum.auto()
    WEST = enum.auto()


class MoveType(enum.IntEnum):
    UNKNOWN = 0
    SLIDE = 1
    JUMP = 2

    @staticmethod
    def from_distance(distance: int) -> "MoveType":
        try:
            return MoveType(distance)
        except ValueError:
            return MoveType.UNKNOWN
