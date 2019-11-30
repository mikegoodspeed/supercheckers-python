import abc
import re

from . import enums, journals, moves, utils


class Player(abc.ABC):
    def __init__(self, team: enums.Team):
        self.team = team

    @abc.abstractmethod
    def create_move(self, journal: journals.Journal) -> moves.Move:
        raise NotImplementedError()


class ConsolePlayer(Player):
    INPUT_REGEX = re.compile("([A-Z][0-9](?:(?:, )|,| ))+[A-Z][0-9]", re.IGNORECASE)
    SPLIT_REGEX = re.compile("(?:(?:, )|,| )")

    def create_move(self, journal: journals.Journal) -> moves.Move:
        while True:
            move_input = input(f"Player {self.team.value} move: ")
            try:
                return self.parse_move_input(move_input)
            except ValueError as e:
                print(str(e))

    def parse_move_input(self, move_input: str) -> moves.Move:
        if not self.INPUT_REGEX.match(move_input):
            raise ValueError(f"Invalid request: {move_input!r}")
        locations = []
        for part in self.SPLIT_REGEX.split(move_input):
            row_id = int(part[1]) - 1
            col_id = utils.to_int(part[0])
            locations.append((row_id, col_id))
        return moves.Move(self.team, locations)
