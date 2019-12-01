import itertools
from dataclasses import dataclass
from typing import Optional

from . import enums, journals, players, rules


@dataclass()
class GameState:
    player_1: players.Player
    player_2: players.Player
    play_state: enums.PlayState = enums.PlayState.NOT_STARTED
    winner: Optional[enums.Team] = None

    def get_current_player(self, journal: journals.Journal) -> players.Player:
        return self.player_1 if journal.current_turn_number % 2 == 0 else self.player_2

    def set_play_state(self, journal: journals.Journal) -> None:
        if journal.current_turn_number > 4:
            board = journal.current_board
            winner = board.get_winner()
            if winner:
                self.play_state = enums.PlayState.COMPLETE
                self.winner = winner


class Game:
    def __init__(self, state: GameState, journal: journals.Journal, verifier: rules.Verifier):
        self.state = state
        self.journal = journal
        self.verifier = verifier

    @property
    def is_active(self) -> bool:
        return self.state.play_state == enums.PlayState.IN_PROGRESS

    def begin(self) -> None:
        print("Beginning game...")
        self.state.play_state = enums.PlayState.IN_PROGRESS
        print(self.journal.current_board)

    def take_turn(self) -> None:
        while True:
            player = self.state.get_current_player(self.journal)
            move = player.create_move(self.journal)
            result = self.verifier.is_valid(self.journal, move)
            if result.is_valid:
                break
            for rule in result.failed_rules:
                print(rule.message)
        self.journal.apply(move)
        self.state.set_play_state(self.journal)
        print(self.journal.current_board)

    def end(self, error: bool = False) -> None:
        if error:
            print("Unhandled error.")
            self.state.play_state = enums.PlayState.ERROR
        elif self.state.winner:
            print(f"Game over, {self.state.winner.value} wins!")
        else:
            print("Game aborted.")
            self.state.play_state = enums.PlayState.COMPLETE

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end(error=bool(exc_val))
