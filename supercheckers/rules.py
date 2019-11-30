import abc
import inspect
import sys
from typing import List

from . import journals, moves


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


class NumLocationsRule(Rule):
    @property
    def message(self) -> str:
        return "Your move must contain two or more locations."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        return len(move.locations) >= 2


class AlwaysOnBoardRule(Rule):
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
