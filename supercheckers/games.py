from dataclasses import dataclass
from typing import Optional

from . import enums, journals, players, verifiers


@dataclass()
class GameState:
    """The state of a Supercheckers game."""

    player_1: players.Player
    player_2: players.Player
    journal: journals.Journal
    play_state: enums.PlayState = enums.PlayState.NOT_STARTED
    winner: Optional[enums.Team] = None

    @property
    def current_player(self) -> players.Player:
        """
        Get the current player based off of the current turn number.

        :return: a Player
        """
        return self.player_1 if self.journal.current_turn_number % 2 != 0 else self.player_2

    def update_play_state(self) -> None:
        """Update the play_state enum based on the state of the game."""
        if self.journal.current_turn_number > 4:
            board = self.journal.current_board
            teams = board.get_middle_teams()
            if not teams:
                self.play_state = enums.PlayState.COMPLETE
                self.winner = None
            elif len(teams) == 1:
                self.play_state = enums.PlayState.COMPLETE
                self.winner = teams.pop()


class Game:
    """A Game of Supercheckers."""

    def __init__(self, state: GameState, verifier: verifiers.Verifier):
        """
        Create a Game of Supercheckers.

        :param state: a Supercheckers GameState
        :param verifier: a rules Verifier
        """
        self.state = state
        self.verifier = verifier

    @property
    def in_progress(self) -> bool:
        """
        Convenience function for determining if the game is still in progress.

        :return: True if the play_state is IN_PROGRESS
        """
        return self.state.play_state == enums.PlayState.IN_PROGRESS

    def begin(self) -> None:
        """Begin a game by setting the play_state to IN_PROGRESS."""
        print("Beginning game...")
        self.state.play_state = enums.PlayState.IN_PROGRESS
        print(self.state.journal.current_board)

    def take_turn(self) -> None:
        """
        Take a single turn.

        This method will not return until a Move is created, validated, and applied.
        """
        player = self.state.current_player
        while True:
            move = player.create_move(self.state.journal.copy())
            result = self.verifier.verify(self.state.journal, move)
            if result.is_valid:
                break
            for rule in result.failed_rules:
                print("ERROR:", rule.message)
        self.state.journal.apply(move)
        self.state.update_play_state()
        print(self.state.journal.current_board)

    def end(self, error: bool = False) -> None:
        """
        End a game.

        If this method is called with error = True, then the play state will be set to ERROR.
        If this method is called while the game is in progress, the game state will be set to COMPLETE.

        :param error: True if an error occurred
        """
        if error:
            print("Game over: unhandled error.")
            self.state.play_state = enums.PlayState.ERROR
        elif self.in_progress:
            print("Game over, game aborted.")
            self.state.play_state = enums.PlayState.COMPLETE
        elif self.state.winner:
            print(f"Game over, {self.state.winner.value} wins!")
        else:
            print("Game over, tie game.")

    def __enter__(self):
        self.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end(error=bool(exc_val))
