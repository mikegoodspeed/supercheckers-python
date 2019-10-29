from dataclasses import dataclass

from .boards import Board
from .enums import PlayState
from .pieces import PieceFactory, PieceCollection
from .players import Player


@dataclass
class GameState:
    play_state: PlayState = PlayState.NOT_STARTED


class Game:
    @classmethod
    def create(cls) -> "Game":
        state = GameState()
        pieces = PieceCollection(PieceFactory())
        board = Board(pieces)
        return cls(state, board)

    def __init__(self, state: GameState, board: Board):
        self.state = state
        self.board = board

    @property
    def is_active(self) -> bool:
        return self.state.play_state == PlayState.NOT_STARTED

    def get_current_player(self) -> Player:
        return None

    def begin(self) -> None:
        print("Beginning game...")

        self.state.play_state = PlayState.IN_PROGRESS
        print(self.board)

    def take_turn(self) -> None:
        player = self.get_current_player()
        while True:
            move = player.create_move()
            if self.board.is_valid(move):
                break
        self.board.apply(move)

    def end(self) -> None:
        print("Game over.")
        self.state.play_state = PlayState.COMPLETE

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()
