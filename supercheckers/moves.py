from dataclasses import dataclass
from typing import List, Tuple

from . import enums


@dataclass(frozen=True)
class Move:
    team: enums.Team
    locations: List[Tuple[int, int]]

    @property
    def is_slide(self):
        return len(self.locations) == 2
