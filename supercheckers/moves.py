from dataclasses import dataclass
from typing import List, Tuple

from . import enums, utils


@dataclass(frozen=True)
class Move:
    team: enums.Team
    locations: List[Tuple[int, int]]

    def __len__(self) -> int:
        return len(self.locations)

    def __str__(self) -> str:
        locations = " ".join(f"{utils.to_char(col_id)}{row_id + 1}" for row_id, col_id in self.locations)
        return f"[{self.team.value}: {locations}]"
