import itertools
from typing import Optional, List, Dict, Iterator

from .enums import Team
from .moves import Move
from .pieces import PieceCollection, Piece


class Board:
    MAX_ROW = 8
    MAX_COL = 8

    def __init__(self, pieces: PieceCollection) -> None:
        self.pieces = pieces
        self.grid: List[List[Optional[Piece]]] = [[None for _ in range(self.MAX_COL)] for _ in range(self.MAX_ROW)]
        self.reset()

    def reset(self) -> None:
        self.pieces.reset()
        team_cycle = itertools.cycle(Team.__members__.values())
        pieces: Dict[Team: Iterator] = {team: iter(self.pieces.active[team]) for team in Team}
        for row_id in range(self.MAX_ROW):
            for col_id in range(self.MAX_COL):
                piece: Optional[Piece] = None
                if not self.in_middle(row_id, col_id):
                    team = next(team_cycle)
                    piece = next(pieces[team])
                self.grid[row_id][col_id] = piece

    @staticmethod
    def in_middle(row_id, col_id) -> bool:
        return (1 < row_id < 6) and (1 < col_id < 6)

    def is_valid(self, move: Move) -> bool:
        pass

    def apply(self, move: Move) -> None:
        pass

    def __str__(self):
        result = []
        for row_id in range(self.MAX_ROW):
            row = []
            for col_id in range(self.MAX_COL):
                piece = self.grid[row_id][col_id]
                row.append(piece.team.value if piece else " ")
            result.append(row)
        return "\n".join("".join(cell for cell in row) for row in result)
