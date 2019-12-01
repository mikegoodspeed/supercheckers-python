import copy
from typing import List, Optional, Tuple

from . import boards, enums, moves


class Journal:
    """A journal of all previous Move and Board states."""

    def __init__(self, board: boards.Board):
        """
        Create a journal.

        :param board: a Board to use as the initial state
        """
        self._log: List[Tuple[Optional[moves.Move], boards.Board]] = [(None, board.copy())]

    @property
    def current_turn_number(self) -> int:
        """
        Return the current turn number.

        The first move returns 1.

        :return: the current turn number
        """
        return len(self._log)

    @property
    def current_team(self) -> enums.Team:
        """
        Return the current team based on the current turn number.

        :return: the current Team
        """
        return enums.Team.ONE if self.current_turn_number % 2 != 0 else enums.Team.TWO

    @property
    def current_board(self) -> boards.Board:
        """
        Return a copy of the current board.

        :return: the current board
        """
        return self._log[-1][1].copy()

    def apply(self, move: moves.Move) -> None:
        """
        Apply a Move to the current_board and save it to the journal.

        This method assumes that the move has been validated.

        :param move: a Move
        """
        board = self.current_board
        board.apply(move)
        self._log.append((move, board))

    def copy(self) -> "Journal":
        """
        Return a deep copy of this journal.

        :return: a Journal
        """
        return copy.deepcopy(self)
