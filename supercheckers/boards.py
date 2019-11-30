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

    def __init__(self, populate: bool = True) -> None:
        self._grid: List[List[Optional[Piece]]] = [[None for _ in range(self.MAX_COL)] for _ in range(self.MAX_ROW)]
        if populate:
            self.reset()

    def reset(self) -> None:
        team_cycle = itertools.cycle(enums.Team.__members__.values())
        for row_id in range(self.MAX_ROW):
            next(team_cycle)
            for col_id in range(self.MAX_COL):
                if not utils.in_middle(row_id, col_id):
                    self._grid[row_id][col_id] = Piece(next(team_cycle), (row_id, col_id))
                else:
                    self._grid[row_id][col_id] = None

    def apply(self, move: moves.Move) -> None:
        for i in range(1, len(move)):
            src_loc = move.locations[i - 1]
            dst_loc = move.locations[i]
            self._move(src_loc, dst_loc)

    def _move(self, src_loc: Tuple[int, int], dst_loc: Tuple[int, int]) -> None:
        src_row, src_col = src_loc
        dst_row, dst_col = dst_loc
        piece = self._grid[src_row][src_col]
        self._grid[src_row][src_col] = None
        self._grid[dst_row][dst_col] = piece
        piece.location = dst_loc

        description = utils.compare(src_loc, dst_loc)
        if abs(description.distance) == 2:
            if description.direction in (enums.Direction.EAST, enums.Direction.WEST):
                jumped_row = src_row
                jumped_col = (src_col + dst_col) // 2
            else:
                jumped_row = (src_row + dst_row) // 2
                jumped_col = src_col
            jumped_piece = self._grid[jumped_row][jumped_col]
            if jumped_piece and jumped_piece.team != piece.team:
                self._grid[jumped_row][jumped_col] = None
                jumped_piece.location = None

    def copy(self) -> "Board":
        return copy.deepcopy(self)

    def __getitem__(self, item: Tuple[int, int]) -> Optional[Piece]:
        row_id, col_id = item
        return self._grid[row_id][col_id]

    def __str__(self) -> str:
        column_row = "   " + " ".join(utils.to_char(col_id) for col_id in range(self.MAX_COL)) + " "
        divider_row = "  +" + ("-" * (self.MAX_COL * 2 - 1)) + "+"

        result = ""
        result += column_row + "\n"
        result += divider_row + "\n"
        for row_id in reversed(range(self.MAX_ROW)):
            result += f"{row_id + 1} |"
            for col_id in range(self.MAX_COL):
                piece = self._grid[row_id][col_id]
                result += piece.team.value if piece else " "
                result += "#" if utils.in_middle(row_id, col_id, extended=True) else "|"
            result += f" {row_id + 1}\n"
        result += divider_row + "\n"
        result += column_row
        return result

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"
