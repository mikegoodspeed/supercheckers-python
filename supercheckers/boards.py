import copy
import itertools
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple

from . import enums, moves, utils


@dataclass
class Piece:
    """A Supercheckers Piece assigned to a team, and optionally a location."""

    team: enums.Team
    location: Optional[Tuple[int, int]] = None


class Board:
    """A Supercheckers Board."""

    MAX_ROW = 8
    MAX_COL = 8

    def __init__(self, populate: bool = True) -> None:
        """
        Create a new game board.

        :param populate: True if the board should be reset to default position.
        """
        self._grid: List[List[Optional[Piece]]] = [
            [None for _ in range(self.MAX_COL)] for _ in range(self.MAX_ROW)
        ]
        if populate:
            self.reset()

    def reset(self) -> None:
        """Reset the board to default position."""
        team_cycle = itertools.cycle(enums.Team.__members__.values())
        for row_id in range(self.MAX_ROW):
            next(team_cycle)
            for col_id in range(self.MAX_COL):
                location = (row_id, col_id)
                self[location] = (
                    None if utils.in_middle(location) else Piece(next(team_cycle))
                )

    def apply(self, move: moves.Move) -> None:
        """
        Apply a Move.

        This method assumes that the move has been validated.

        :param move: a Move
        """
        for i in range(1, len(move)):
            src_loc = move.locations[i - 1]
            dst_loc = move.locations[i]
            self._move(src_loc, dst_loc)

    def _move(self, src_loc: Tuple[int, int], dst_loc: Tuple[int, int]) -> None:
        """
        Move from a source location to a destination location.

        :param src_loc: a (row_id, col_id) source location
        :param dst_loc: a (row_id, col_id) destination location
        """
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
        """
        Return a set of all the Teams that are in the middle of the board.

        :return: a set of Team enums
        """
        teams = set()
        for location in itertools.product(range(self.MAX_ROW), range(self.MAX_COL)):
            if utils.in_middle(location):
                piece = self[location]
                if piece:
                    teams.add(piece.team)
        return teams

    def copy(self) -> "Board":
        """
        Return a deep copy of this board.

        :return: a Board
        """
        return copy.deepcopy(self)

    def __getitem__(self, item: Tuple[int, int]) -> Optional[Piece]:
        """
        Get a piece at a location, returning None of there is no piece at that location.

        :param item: a (row_id, col_id) location
        :return: Piece at that location, or None
        :raise: ValueError if location is invalid
        """
        row_id, col_id = item
        if not ((0 <= row_id < self.MAX_ROW) and (0 <= col_id < self.MAX_COL)):
            raise ValueError(f"Invalid location: {item!r}")
        return self._grid[row_id][col_id]

    def __setitem__(self, key: Tuple[int, int], value: Optional[Piece]) -> None:
        """
        Set a piece at a location and update that piece's location.

        :param key: a (row_id, col_id) location
        :param value: a Piece to set, or None to unset
        :raise: ValueError if location is invalid
        """
        row_id, col_id = key
        if not ((0 <= row_id < self.MAX_ROW) and (0 <= col_id < self.MAX_COL)):
            raise ValueError(f"Invalid location: {key!r}")
        self._grid[row_id][col_id] = value
        if value:
            value.location = key

    def __str__(self) -> str:
        """
        Return a graphical representation of the current board state.

        :return: an ascii board string
        """
        col_names = [utils.to_char(col_id) for col_id in range(self.MAX_COL)]
        column_row = "   " + " ".join(col_names) + " "
        divider_row = "  +" + ("-" * (self.MAX_COL * 2 - 1)) + "+"

        result = ""
        result += column_row + "\n"
        result += divider_row + "\n"
        for row_id in reversed(range(self.MAX_ROW)):
            result += f"{row_id + 1} |"
            for col_id in range(self.MAX_COL):
                piece = self[(row_id, col_id)]
                result += piece.team.value if piece else " "
                result += "#" if (1 < row_id < 6) and (1 <= col_id < 6) else "|"
            result += f" {row_id + 1}\n"
        result += divider_row + "\n"
        result += column_row
        return result

    def __repr__(self) -> str:
        """
        Return the internal representation of this Board.

        :return: a repr string
        """
        return f"{self.__class__.__qualname__}()"
