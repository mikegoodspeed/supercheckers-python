from dataclasses import dataclass
from typing import Optional, Tuple

from . import enums


@dataclass(frozen=True)
class Description:
    direction: enums.Direction
    move_type: enums.MoveType
    jmp_loc: Optional[Tuple[int, int]]


def compare(src_loc: Tuple[int, int], dst_loc: Tuple[int, int]) -> Description:
    src_row, src_col = src_loc
    dst_row, dst_col = dst_loc
    horizontal = src_row == dst_row
    vertical = src_col == dst_col
    if horizontal == vertical:  # same spot or neither vertical nor horizontal
        return Description(enums.Direction.UNKNOWN, enums.MoveType.UNKNOWN, None)
    if horizontal:
        direction = enums.Direction.EAST if src_col < dst_col else enums.Direction.WEST
        distance = dst_col - src_col
        jmp_loc = (src_row, src_col + (distance // 2)) if abs(distance) == 2 else None
    else:
        direction = enums.Direction.NORTH if src_row < dst_row else enums.Direction.SOUTH
        distance = dst_row - src_row
        jmp_loc = (src_row + (distance // 2), src_col) if abs(distance) == 2 else None
    move_type = enums.MoveType.from_distance(abs(distance))
    return Description(direction, move_type, jmp_loc)


def in_middle(location: Tuple[int, int], *, extended: bool = False) -> bool:
    row_id, col_id = location
    if extended:
        return (1 < row_id < 6) and (1 <= col_id < 6)
    return (1 < row_id < 6) and (1 < col_id < 6)


def to_int(value: str) -> int:
    return ord(value.upper()) - ord("A")


def to_char(value: int) -> str:
    return chr(ord("A") + value)
