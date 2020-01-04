from dataclasses import dataclass
from typing import Optional, Tuple

from . import enums


@dataclass(frozen=True)
class Description:
    """A Description of two locations."""

    direction: enums.Direction
    move_type: enums.MoveType
    jmp_loc: Optional[Tuple[int, int]]


def compare(src_loc: Tuple[int, int], dst_loc: Tuple[int, int]) -> Description:
    """
    Compare the relationship between two locations.

    If they are aligned horizontal or vertical, then the result will have a direction.
    If they are separated by a slide or a jump, then the result will have a move type.
    If they are a jump apart, then the result will have a jumped location.

    :param src_loc: a (row_id, col_id) source location
    :param dst_loc: a (row_id, col_id) destination location
    :return: a Description of the locations
    """
    src_row, src_col = src_loc
    dst_row, dst_col = dst_loc
    horizontal = src_row == dst_row
    vertical = src_col == dst_col
    if horizontal == vertical:
        return Description(enums.Direction.UNKNOWN, enums.MoveType.UNKNOWN, None)
    if horizontal:
        if src_col < dst_col:
            direction = enums.Direction.EAST
        else:
            direction = enums.Direction.WEST
        distance = dst_col - src_col
        jmp_loc = (src_row, src_col + (distance // 2)) if abs(distance) == 2 else None
    else:
        if src_row < dst_row:
            direction = enums.Direction.NORTH
        else:
            direction = enums.Direction.SOUTH
        distance = dst_row - src_row
        jmp_loc = (src_row + (distance // 2), src_col) if abs(distance) == 2 else None
    move_type = enums.MoveType.from_distance(abs(distance))
    return Description(direction, move_type, jmp_loc)


def in_middle(location: Tuple[int, int]) -> bool:
    """
    Determine if a location is in the middle of the Board.

    :param location: a (row_id, col_id) location
    :return: True if the location is in the middle of the Board
    """
    row_id, col_id = location
    return (1 < row_id < 6) and (1 < col_id < 6)


def to_int(value: str) -> int:
    """
    Convert a single character to an integer, where A equals 0.

    Note: This method is case insensitive.

    :param value: a character
    :return: an integer representation
    """
    return ord(value.upper()) - ord("A")


def to_char(value: int) -> str:
    """
    Convert an integer to a single character, where 0 equals A.

    Note: This method will return an uppercase character.

    :param value: an integer
    :return: a character representation
    """
    return chr(ord("A") + value)
