import abc

from .enums import Team
from .moves import Move


class Player(abc.ABC):
    def __init__(self, team: Team):
        self.team = team

    @abc.abstractmethod
    def create_move(self) -> Move:
        pass
