from dataclasses import dataclass
from typing import Sequence, Tuple

from . import enums, utils


@dataclass(frozen=True)
class Move:
    """A single Supercheckers move represented by a team and a sequence of locations."""

    team: enums.Team
    locations: Sequence[Tuple[int, int]]

    def __len__(self) -> int:
        """
        Return the length of the Love, which is the number of locations in the move.

        :return: the number of locations
        """
        return len(self.locations)

    def __str__(self) -> str:
        """
        Return a human-readable representation of a Move.

        :return: a readable Move string
        """
        locations = " ".join(
            f"{utils.to_char(col_id)}{row_id + 1}" for row_id, col_id in self.locations
        )
        return f"[{self.team.value}: {locations}]"
