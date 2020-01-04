import abc
import re

from . import enums, journals, moves, utils


class Player(abc.ABC):
    """An abstract base class representing the interface of a Player."""

    def __init__(self, team: enums.Team):
        """
        Create a new player associated with a team.

        :param team: a Team
        """
        self.team = team

    @abc.abstractmethod
    def create_move(self, journal: journals.Journal) -> moves.Move:
        """
        Create a Move, given a Journal's history of the game.

        :param journal: a Game Journal
        :return: a Move
        """
        raise NotImplementedError()


class ConsolePlayer(Player):
    """A Player that creates a move by entering text on the console."""

    INPUT_REGEX = re.compile("^([A-Z][0-9][, ] *)+[A-Z][0-9]$", re.IGNORECASE)
    SPLIT_REGEX = re.compile("[, ] *")

    def create_move(self, journal: journals.Journal) -> moves.Move:
        while True:
            move_input = input(f"Player {self.team.value} move: ")
            try:
                return self.parse_move_input(move_input.strip(" "))
            except ValueError as e:
                print("ERROR:", str(e))

    def parse_move_input(self, move_input: str) -> moves.Move:
        """
        Parse an input string into a Move.

        This method is case insensitive. If the move is not in an acceptable format, a
        ValueError is thrown.

        Acceptable formats:
        * "c2 c4"
        * "c2, c4"
        * "c2,c4"
        " "  c2  e4  "
        * "c2 c4 c6"
        * "C2 C4"
        * "C2 c4 C6"

        :param move_input: a string representing a Move
        :return: a Move
        :raise: ValueError if the move_input can not be parsed
        """
        if not self.INPUT_REGEX.match(move_input):
            raise ValueError(f"Invalid request: {move_input!r}")
        locations = []
        for part in self.SPLIT_REGEX.split(move_input):
            row_id = int(part[1]) - 1
            col_id = utils.to_int(part[0])
            locations.append((row_id, col_id))
        return moves.Move(self.team, locations)
