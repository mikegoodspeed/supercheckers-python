import abc
import inspect
import sys
from typing import Iterable

from . import enums, journals, moves, utils


class Rule(abc.ABC):
    """An abstract base class that represents the interface for a rule."""

    @property
    @abc.abstractmethod
    def message(self) -> str:
        """
        Return the message for the rule, suitable to be displayed when the rule fails.

        :return: a message string
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        """
        Validate a move based on the Game Journal.

        :param journal: a Game Journal
        :param move: a Move to validate
        :return: True if the Move is valid
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        """
        Return the internal representation of this Rule.

        :return: a repr string
        """
        return f"{self.__class__.__qualname__}()"


class AtLeastTwoLocationsRule(Rule):
    """Rule requiring a Move to have at least two locations."""

    @property
    def message(self) -> str:
        return "Your move must contain at least two locations."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        return len(move) >= 2


class ExactlyTwoLocationsRule(Rule):
    """Rule requiring a Move with two locations has either a slide or a jump."""

    @property
    def message(self) -> str:
        return (
            "A move with two locations must be either a slide (one space) or a jump "
            "(two spaces) in a straight line. "
        )

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        if len(move) != 2:
            return True
        src_loc, dst_loc = move.locations
        description = utils.compare(src_loc, dst_loc)
        return description.move_type is not enums.MoveType.UNKNOWN


class MoreThanTwoLocationsRule(Rule):
    """Rule requiring a Move with more than two locations has only jumps."""

    @property
    def message(self) -> str:
        return (
            "A move with more than two locations must contain only jumps (two spaces)."
        )

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
    """Rule requiring a Move never leaves the board."""

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
    """Rule requiring a Move manipulates a piece from the correct team."""

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


class IntermediateLandingLocationsRule(Rule):
    """Rule requiring a Move's intermediate locations be empty."""

    @property
    def message(self) -> str:
        return "All intermediate landing locations must be empty."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        if len(move) <= 2:
            return True
        board = journal.current_board
        for location in move.locations[1:-1]:
            if board[location] is not None:
                return False
        return True


class FinalLandingLocationRule(Rule):
    """Rule requiring a Move's final location be empty."""

    @property
    def message(self) -> str:
        return "Your final landing location must be empty."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        if len(move) <= 1:
            return True
        return journal.current_board[move.locations[-1]] is None


class FirstFourMovesRule(Rule):
    """Rule requiring the first four Moves be slides into the middle of the board."""

    @property
    def message(self) -> str:
        return "For your first two moves, you must slide into the middle."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        if journal.current_turn_number > 4:
            return True
        if len(move) != 2:
            return False
        src_loc, dst_loc = move.locations
        description = utils.compare(src_loc, dst_loc)
        if description.move_type != enums.MoveType.SLIDE:
            return False
        if not utils.in_middle(dst_loc):
            return False
        return True


class JumpOverAPieceRule(Rule):
    """Rule requiring a Move's jumps to occur over a piece."""

    @property
    def message(self) -> str:
        return "All jumps must be over a piece."

    def is_valid(self, journal: journals.Journal, move: moves.Move) -> bool:
        team = journal.current_team
        board = journal.current_board
        for i in range(1, len(move.locations)):
            src_loc = move.locations[i - 1]
            dst_loc = move.locations[i]
            description = utils.compare(src_loc, dst_loc)
            if description.move_type == enums.MoveType.JUMP:
                jmp_loc = description.jmp_loc
                assert jmp_loc
                jmp_piece = board[jmp_loc]
                if jmp_piece is None:
                    return False
                if jmp_piece.team != team:
                    board[jmp_loc] = None
        return True


def all_rules() -> Iterable[Rule]:
    """
    Return all instances of Rules defined in this module in alphabetical order.

    :return: an Iterable of Rules
    """

    def is_concrete_rule_class(obj):
        """
        Determine if object is a concrete class that is a subclass of Rule.

        :param obj: any object
        :return: True if object is a concrete class that is a subclass of Rule
        """
        return (
            inspect.isclass(obj)
            and not inspect.isabstract(obj)
            and issubclass(obj, Rule)
        )

    current_module = sys.modules[__name__]
    rule_classes = inspect.getmembers(current_module, is_concrete_rule_class)
    return [rule_class() for name, rule_class in rule_classes]
