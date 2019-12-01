from typing import List, Optional, Tuple

from . import boards, enums, moves


class Journal:
    def __init__(self, board: boards.Board):
        self._log: List[Tuple[Optional[moves.Move], boards.Board]] = [(None, board.copy())]

    @property
    def current_turn_number(self) -> int:
        return len(self._log) + 1

    @property
    def current_team(self) -> enums.Team:
        return enums.Team.ONE if self.current_turn_number % 2 == 0 else enums.Team.TWO

    @property
    def current_board(self) -> boards.Board:
        return self._log[-1][1].copy()

    def apply(self, move: moves.Move) -> None:
        board = self.current_board
        board.apply(move)
        self._log.append((move, board))
