import itertools
from dataclasses import dataclass

from .boards import Board
from .enums import PlayState
from .players import Player


@dataclass
class GameState:
    play_state: PlayState = PlayState.NOT_STARTED


class Game:
    def __init__(self, state: GameState, board: Board, player_1: Player, player_2: Player):
        self.state = state
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2
        self._player_cycle = itertools.cycle((player_1, player_2))
        self.current_player = next(self._player_cycle)

    @property
    def is_active(self) -> bool:
        return self.state.play_state == PlayState.IN_PROGRESS

    def begin(self) -> None:
        print("Beginning game...")

        self.state.play_state = PlayState.IN_PROGRESS
        print(self.board)

    def take_turn(self) -> None:
        while True:
            move = self.current_player.create_move()
            if self.board.is_valid(move):
                break
        self.board.apply(move)
        print(self.board)
        self.current_player = next(self._player_cycle)

    def end(self, error: bool = False) -> None:
        if error:
            print("Unhandled error.")
            self.state.play_state = PlayState.ERROR
        else:
            print("Game over.")
            self.state.play_state = PlayState.COMPLETE

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end(error=bool(exc_val))
