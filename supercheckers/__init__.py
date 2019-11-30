from .__meta__ import __author__, __description__, __license__, __title__, __version__
from .boards import Board, Piece
from .enums import PlayState, Team
from .games import Game, GameState
from .players import ConsolePlayer, Move, Player

# Generate all script:
#
# import supercheckers as sc
# whitelist = ["__author__", "__description__", "__license__", "__title__", "__version__"]
# print(sorted(i for i in dir(sc) if callable(getattr(sc, i)) or i in whitelist))

__all__ = [
    "Board",
    "ConsolePlayer",
    "Game",
    "GameState",
    "Move",
    "Piece",
    "PlayState",
    "Player",
    "Team",
    "__author__",
    "__description__",
    "__license__",
    "__title__",
    "__version__",
]
