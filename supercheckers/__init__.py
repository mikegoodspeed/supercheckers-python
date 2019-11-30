from .__meta__ import __author__, __description__, __license__, __title__, __version__
from .boards import Board, Piece
from .enums import PlayState, Team
from .games import Game, GameState
from .journals import Journal
from .moves import Move
from .players import ConsolePlayer, Player
from .rules import Result, Rule, Verifier, all_rules
from .utils import in_middle, to_char, to_int

"""
# Generate all script
import supercheckers as sc
whitelist = ["__author__", "__description__", "__license__", "__title__", "__version__"]
print(sorted(i for i in dir(sc) if callable(getattr(sc, i)) or i in whitelist))
"""

__all__ = [
    "Board",
    "ConsolePlayer",
    "Game",
    "GameState",
    "Journal",
    "Move",
    "Piece",
    "PlayState",
    "Player",
    "Result",
    "Rule",
    "Team",
    "Verifier",
    "__author__",
    "__description__",
    "__license__",
    "__title__",
    "__version__",
    "all_rules",
    "in_middle",
    "to_char",
    "to_int",
]
