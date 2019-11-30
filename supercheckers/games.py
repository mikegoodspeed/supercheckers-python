import itertools
from dataclasses import dataclass

from . import boards, enums, players


@dataclass
class GameState:
    play_state: enums.PlayState = enums.PlayState.NOT_STARTED


class Game:
    def __init__(self, state: GameState, board: boards.Board, player_1: players.Player, player_2: players.Player):
        self.state = state
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2
        self._player_cycle = itertools.cycle((player_1, player_2))
        self.current_player = next(self._player_cycle)

    @property
    def is_active(self) -> bool:
        return self.state.play_state == enums.PlayState.IN_PROGRESS

    def begin(self) -> None:
        print("Beginning game...")

        self.state.play_state = enums.PlayState.IN_PROGRESS
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
            self.state.play_state = enums.PlayState.ERROR
        else:
            print("Game over.")
            self.state.play_state = enums.PlayState.COMPLETE

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end(error=bool(exc_val))
