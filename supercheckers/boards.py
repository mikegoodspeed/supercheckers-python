import itertools
from dataclasses import dataclass
from typing import List, Optional, Tuple

from . import enums, players, utils


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
                if not self.in_middle(row_id, col_id):
                    self.grid[row_id][col_id] = Piece(next(team_cycle), (row_id, col_id))
                else:
                    self.grid[row_id][col_id] = None

    @staticmethod
    def in_middle(row_id, col_id) -> bool:
        return (1 < row_id < 6) and (1 < col_id < 6)

    def is_valid(self, move: players.Move) -> bool:
        pass

    def apply(self, move: players.Move) -> None:
        pass

    def __str__(self):
        def in_middle(rid: int, cid: int) -> bool:
            return (1 < rid < 6) and (1 <= cid < 6)

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
                result += "#" if in_middle(row_id, col_id) else "|"
            result += f" {row_id + 1}\n"
        result += divider_row + "\n"
        result += column_row
        return result
