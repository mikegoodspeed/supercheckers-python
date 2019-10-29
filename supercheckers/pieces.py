import collections
from dataclasses import dataclass
from typing import Dict, List

from .enums import Team


@dataclass
class Piece:
    team: Team


class PieceFactory:
    @staticmethod
    def create(team: Team):
        return Piece(team)


class PieceCollection:
    PIECES_PER_TEAM = 24

    def __init__(self, factory: PieceFactory):
        self.factory = factory
        self.active: Dict[Team, List[Piece]] = collections.defaultdict(list)
        self.inactive: Dict[Team, List[Piece]] = collections.defaultdict(list)
        self.reset()

    def reset(self):
        self.active.clear()
        self.inactive.clear()
        for i in range(self.PIECES_PER_TEAM):
            for team in Team:
                piece = self.factory.create(team)
                self.active[team].append(piece)
