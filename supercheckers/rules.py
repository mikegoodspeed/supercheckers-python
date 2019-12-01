import abc
import inspect
import sys
from typing import List

from . import enums, journals, moves, utils


class Rule(abc.ABC):
    @property
    @abc.abstractmethod
    def message(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"


class AtLeastTwoLocationsRule(Rule):
    @property
    def message(self) -> str:
        return "Your move must contain at least two locations."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        return len(move) >= 2


class ExactlyTwoLocationsRule(Rule):
    @property
    def message(self) -> str:
        return "A move with two locations must be either a slide (one space) or a jump (two spaces)."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        if len(move) != 2:
            return True
        src_loc, dst_loc = move.locations
        description = utils.compare(src_loc, dst_loc)
        return description.move_type is not enums.MoveType.UNKNOWN


class MoreThanTwoLocationsRule(Rule):
    @property
    def message(self) -> str:
        return "A move with more than two locations must contain only jumps (two spaces)."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        if len(move) <= 2:
            return True
        for i in range(1, len(move)):
            src_loc = move.locations[i - 1]
            dst_loc = move.locations[i]
            description = utils.compare(src_loc, dst_loc)
            if description.move_type != enums.MoveType.JUMP:
                return False
        return True


class AlwaysOnTheBoardRule(Rule):
    @property
    def message(self) -> str:
        return "Your piece must remain on the board at all times."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        board = journal.current_board
        for location in move.locations:
            row_id, col_id = location
            if not (0 <= row_id < board.MAX_ROW):
                return False
            if not (0 <= col_id < board.MAX_COL):
                return False
        return True


class CorrectTeamRule(Rule):
    @property
    def message(self) -> str:
        return "You must move a piece from your own team."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        board = journal.current_board
        if not move.locations:
            return False
        piece = board[move.locations[0]]
        if not piece:
            return False
        if piece.team != journal.current_team:
            return False
        return True


class IntermittentEmptySpacesRule(Rule):
    @property
    def message(self) -> str:
        return "All intermittent locations must be empty."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        if len(move) <= 2:
            return True
        board = journal.current_board
        for location in move.locations[1:-1]:
            if board[location] is not None:
                return False
        return True


class EndOnEmptyRule(Rule):
    @property
    def message(self) -> str:
        return "You must land on an empty location."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        if len(move) <= 1:
            return True
        return journal.current_board[move.locations[-1]] is None


class Result:
    def __init__(self, failed_rules: List[Rule]):
        self.failed_rules = failed_rules

    @property
    def is_valid(self) -> bool:
        return not bool(self.failed_rules)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.failed_rules!r})"


class Verifier:
    def __init__(self, rules: List[Rule]):
        assert rules
        self.rules = rules

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> Result:
        invalid_rules = []
        for rule in self.rules:
            if not rule.is_valid(journal, move):
                invalid_rules.append(rule)
        return Result(invalid_rules)


def all_rules() -> List[Rule]:
    def is_concrete_rule(obj):
        return inspect.isclass(obj) and not inspect.isabstract(obj) and issubclass(obj, Rule)

    current_module = sys.modules[__name__]
    return [member() for name, member in inspect.getmembers(current_module, is_concrete_rule)]
