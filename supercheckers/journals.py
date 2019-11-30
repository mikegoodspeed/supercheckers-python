from typing import List, Optional, Tuple

from . import boards, enums, moves


class Journal:
    def __init__(self, board: boards.Board):
        self.log: List[Tuple[Optional[moves.Move], boards.Board]] = [(None, board.copy())]

    @property
    def current_turn_number(self) -> int:
        return len(self.log) + 1

    @property
    def current_team(self) -> enums.Team:
        return enums.Team.ONE if self.current_turn_number % 1 == 0 else enums.Team.TWO

    @property
    def current_board(self) -> boards.Board:
        return self.log[-1][1].copy()

    def apply(self, move: moves.Move) -> None:
        board = self.current_board
        board.apply(move)
        self.log.append((move, board))
