import abc
import re
from dataclasses import dataclass
from typing import List, Tuple

from . import enums, utils


@dataclass(frozen=True)
class Move:
    team: enums.Team
    locations: List[Tuple[int, int]]

    @property
    def is_slide(self):
        return len(self.locations) == 2


class Player(abc.ABC):
    def __init__(self, team: enums.Team):
        self.team = team

    @abc.abstractmethod
    def create_move(self) -> Move:
        raise NotImplementedError()


class ConsolePlayer(Player):
    INPUT_REGEX = re.compile("([A-Z][0-9]((, )|,| )?){2,}", re.IGNORECASE)
    SPLIT_REGEX = re.compile("(?:(?:, )|,| )")

    def create_move(self) -> Move:
        move_input = input(f"Player {self.team.value} move: ")
        return self.parse_move_input(move_input)

    def parse_move_input(self, move_input: str) -> Move:
        if not self.INPUT_REGEX.match(move_input):
            raise ValueError(f"Invalid request: {move_input!r}")
        locations = []
        for part in self.SPLIT_REGEX.split(move_input):
            row_id = int(part[1]) - 1
            col_id = utils.to_int(part[0])
            locations.append((row_id, col_id))
        return Move(self.team, locations)
