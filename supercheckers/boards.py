import copy
import itertools
from dataclasses import dataclass
from typing import List, Optional, Tuple, Set

from . import enums, moves, utils


@dataclass
class Piece:
    team: enums.Team
    location: Optional[Tuple[int, int]] = None


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
                location = (row_id, col_id)
                self[location] = None if utils.in_middle(location) else Piece(next(team_cycle))

    def apply(self, move: moves.Move) -> None:
        for i in range(1, len(move)):
            src_loc = move.locations[i - 1]
            dst_loc = move.locations[i]
            self._move(src_loc, dst_loc)

    def _move(self, src_loc: Tuple[int, int], dst_loc: Tuple[int, int]) -> None:
        piece = self[src_loc]
        assert piece and piece.team
        self[src_loc] = None
        self[dst_loc] = piece

        description = utils.compare(src_loc, dst_loc)
        if description.move_type == enums.MoveType.JUMP:
            assert description.jmp_loc
            jmp_piece = self[description.jmp_loc]
            assert jmp_piece and jmp_piece.team
            if jmp_piece.team != piece.team:
                self[description.jmp_loc] = None

    def get_middle_teams(self) -> Set[enums.Team]:
        teams = set()
        for location in itertools.product(range(self.MAX_ROW), range(self.MAX_COL)):
            if utils.in_middle(location):
                piece = self[location]
                if piece:
                    teams.add(piece.team)
        return teams

    def copy(self) -> "Board":
        return copy.deepcopy(self)

    def __getitem__(self, item: Tuple[int, int]) -> Optional[Piece]:
        row_id, col_id = item
        return self._grid[row_id][col_id]

    def __setitem__(self, key: Tuple[int, int], value: Optional[Piece]) -> None:
        row_id, col_id = key
        self._grid[row_id][col_id] = value
        if value:
            value.location = key

    def __str__(self) -> str:
        column_row = "   " + " ".join(utils.to_char(col_id) for col_id in range(self.MAX_COL)) + " "
        divider_row = "  +" + ("-" * (self.MAX_COL * 2 - 1)) + "+"

        result = ""
        result += column_row + "\n"
        result += divider_row + "\n"
        for row_id in reversed(range(self.MAX_ROW)):
            result += f"{row_id + 1} |"
            for col_id in range(self.MAX_COL):
                location = (row_id, col_id)
                piece = self[location]
                result += piece.team.value if piece else " "
                result += "#" if utils.in_middle(location, extended=True) else "|"
            result += f" {row_id + 1}\n"
        result += divider_row + "\n"
        result += column_row
        return result

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"
