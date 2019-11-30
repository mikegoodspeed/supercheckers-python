import copy
import itertools
from dataclasses import dataclass
from typing import List, Optional, Tuple

from . import enums, moves, utils


@dataclass
class Piece:
    team: enums.Team
    location: Optional[Tuple[int, int]]


class Board:
    MAX_ROW = 8
    MAX_COL = 8
    COL_NAMES = [utils.to_char(col_id + 1) for col_id in range(MAX_COL)]

    def __init__(self) -> None:
        self.grid: List[List[Optional[Piece]]] = [[None for _ in range(self.MAX_COL)] for _ in range(self.MAX_ROW)]
        self.reset()

    def reset(self) -> None:
        team_cycle = itertools.cycle(enums.Team.__members__.values())
        for row_id in range(self.MAX_ROW):
            for col_id in range(self.MAX_COL):
                if not utils.in_middle(row_id, col_id):
                    self.grid[row_id][col_id] = Piece(next(team_cycle), (row_id, col_id))
                else:
                    self.grid[row_id][col_id] = None

    def apply(self, move: moves.Move) -> None:
        pass

    def copy(self) -> "Board":
        return copy.deepcopy(self)

    def __str__(self):
        column_row = "   " + " ".join(self.COL_NAMES) + " "
        divider_row = "  +" + ("-" * (self.MAX_COL * 2 - 1)) + "+"

        result = ""
        result += column_row + "\n"
        result += divider_row + "\n"
        for row_id in reversed(range(self.MAX_ROW)):
            result += f"{row_id + 1} |"
            for col_id in range(self.MAX_COL):
                piece = self.grid[row_id][col_id]
                result += piece.team.value if piece else " "
                result += "#" if utils.in_middle(row_id, col_id, extended=True) else "|"
            result += f" {row_id + 1}\n"
        result += divider_row + "\n"
        result += column_row
        return result
