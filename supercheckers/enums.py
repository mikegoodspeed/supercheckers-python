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
    IDENTICAL = enum.auto()
    NORTH = enum.auto()
    SOUTH = enum.auto()
    EAST = enum.auto()
    WEST = enum.auto()
