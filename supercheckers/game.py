import enum
from dataclasses import dataclass

from . import board as board_


class PlayState(enum.Enum):
    NOT_STARTED = enum.auto()
    IN_PROGRESS = enum.auto()
    COMPLETE = enum.auto()


@dataclass
class GameState:
    play_state: PlayState = PlayState.NOT_STARTED


class Game:
    def __init__(self, state: GameState = None, board: board_.Board = None):
        self.state = state or GameState()
        self.board = board or board_.Board()

    @property
    def is_active(self) -> bool:
        return self.state.play_state == PlayState.NOT_STARTED

    def begin(self) -> None:
        print("Beginning game...")
        self.state.play_state = PlayState.IN_PROGRESS

    def take_turn(self) -> None:
        pass
        # player = self.get_current_player()
        # while True:
        #     move = player.create_move()
        #     if self.board.is_valid(move):
        #         break
        # self.board.apply(move)

    def end(self) -> None:
        print("Game over.")
        self.state.play_state = PlayState.COMPLETE
