import abc
import re
from dataclasses import dataclass
from typing import List

from .enums import Team
from .utils import to_int


@dataclass(frozen=True)
class Location:
    row_id: int
    col_id: int


@dataclass(frozen=True)
class Move:
    locations: List[Location]

    @property
    def is_slide(self):
        return len(self.locations) == 2


class Player(abc.ABC):
    def __init__(self, team: Team):
        self.team = team

    @abc.abstractmethod
    def create_move(self) -> Move:
        raise NotImplementedError()


class ConsolePlayer(Player):
    INPUT_REGEX = re.compile("([A-Z][0-9]((, )|,| )?){2,}", re.IGNORECASE)
    SPLIT_REGEX = re.compile("(?:(?:, )|,| )")

    def create_move(self) -> Move:
        move_input = input(f"Player {self.team.value} move:")
        return self.parse_move_input(move_input)

    def parse_move_input(self, move_input: str) -> Move:
        if not self.INPUT_REGEX.match(move_input):
            raise ValueError(f"Invalid request: {move_input!r}")
        parts = self.SPLIT_REGEX.split(move_input)
        return Move([Location(int(part[1]), to_int(part[0])) for part in parts])
