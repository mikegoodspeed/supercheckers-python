from dataclasses import dataclass
from typing import Optional, Tuple

from . import enums


@dataclass(frozen=True)
class Description:
    direction: enums.Direction
    distance: Optional[int]


def compare(src_loc: Tuple[int, int], dst_loc: Tuple[int, int]) -> Description:
    if src_loc == dst_loc:
        return Description(enums.Direction.IDENTICAL, 0)
    src_row, src_col = src_loc
    dst_row, dst_col = dst_loc
    if src_row == dst_row:
        direction = enums.Direction.EAST if src_col < dst_col else enums.Direction.WEST
        distance = dst_col - src_col
        return Description(direction, distance)
    if src_col == dst_col:
        direction = enums.Direction.NORTH if src_row < dst_row else enums.Direction.SOUTH
        distance = dst_row - src_row
        return Description(direction, distance)
    return Description(enums.Direction.UNKNOWN, None)


def in_middle(row_id, col_id, *, extended: bool = False) -> bool:
    if extended:
        return (1 < row_id < 6) and (1 <= col_id < 6)
    return (1 < row_id < 6) and (1 < col_id < 6)


def to_int(value: str) -> int:
    return ord(value.upper()) - ord("A")


def to_char(value: int) -> str:
    return chr(ord("A") + value)
