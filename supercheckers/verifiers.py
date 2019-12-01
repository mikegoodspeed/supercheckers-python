from dataclasses import dataclass
from typing import Iterable

from . import journals, moves, rules


@dataclass
class Result:
    """A Result of a Verifier's Move verification check."""

    failed_rules: Iterable[rules.Rule]

    @property
    def is_valid(self) -> bool:
        return not bool(self.failed_rules)


class Verifier:
    """A Move Verifier."""

    def __init__(self, all_rules: Iterable[rules.Rule]):
        """
        Create a Move Verifier with an Iterable of Rules.

        :param all_rules: the Rules that will be checked.
        """
        assert all_rules
        self.all_rules = all_rules

    def verify(self, journal: journals.Journal, move: moves.Move) -> Result:
        """
        Given a Journal, verify a Move against all rules.

        :param journal: a Game Journal
        :param move: a Move to validate
        :return: a Result, containing failed_rules
        """
        failed_rules = []
        for rule in self.all_rules:
            if not rule.is_valid(journal, move):
                failed_rules.append(rule)
        return Result(failed_rules)
