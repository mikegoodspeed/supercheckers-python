import pytest

import supercheckers as sc
from supercheckers import utils


@pytest.mark.parametrize(
    "src_loc, dst_loc, direction, move_type, jmp_loc",
    [
        ((5, 5), (7, 5), sc.Direction.NORTH, sc.MoveType.JUMP, (6, 5)),
        ((5, 5), (3, 5), sc.Direction.SOUTH, sc.MoveType.JUMP, (4, 5)),
        ((5, 5), (5, 7), sc.Direction.EAST, sc.MoveType.JUMP, (5, 6)),
        ((5, 5), (5, 3), sc.Direction.WEST, sc.MoveType.JUMP, (5, 4)),
        ((5, 5), (6, 5), sc.Direction.NORTH, sc.MoveType.SLIDE, None),
        ((5, 5), (4, 5), sc.Direction.SOUTH, sc.MoveType.SLIDE, None),
        ((5, 5), (5, 6), sc.Direction.EAST, sc.MoveType.SLIDE, None),
        ((5, 5), (5, 4), sc.Direction.WEST, sc.MoveType.SLIDE, None),
        ((5, 5), (5, 5), sc.Direction.UNKNOWN, sc.MoveType.UNKNOWN, None),
        ((5, 5), (6, 6), sc.Direction.UNKNOWN, sc.MoveType.UNKNOWN, None),
        ((5, 5), (4, 4), sc.Direction.UNKNOWN, sc.MoveType.UNKNOWN, None),
        ((5, 5), (6, 4), sc.Direction.UNKNOWN, sc.MoveType.UNKNOWN, None),
        ((5, 5), (4, 6), sc.Direction.UNKNOWN, sc.MoveType.UNKNOWN, None),
    ],
)
def test_compare_east(src_loc, dst_loc, direction, move_type, jmp_loc):
    result = utils.compare(src_loc, dst_loc)
    assert result == utils.Description(direction, move_type, jmp_loc)


@pytest.mark.parametrize("row_id", [0, 1, 2, 3, 4, 5, 6, 7, 8])
@pytest.mark.parametrize("col_id", [0, 1, 2, 3, 4, 5, 6, 7, 8])
def test_in_middle(row_id, col_id):
    expected = (2 <= row_id <= 5) and (2 <= col_id <= 5)
    assert utils.in_middle((row_id, col_id)) is expected


@pytest.mark.parametrize("row_id", [0, 1, 2, 3, 4, 5, 6, 7, 8])
@pytest.mark.parametrize("col_id", [0, 1, 2, 3, 4, 5, 6, 7, 8])
def test_in_middle_extended(row_id, col_id):
    expected = (2 <= row_id <= 5) and (1 <= col_id <= 5)
    assert utils.in_middle((row_id, col_id), extended=True) is expected


@pytest.mark.parametrize(
    "value, expected", [("A", 0), ("B", 1), ("C", 2), ("D", 3), ("E", 4), ("F", 5), ("G", 6), ("H", 7)],
)
def test_to_int_upper(value, expected):
    assert utils.to_int(value) == expected


@pytest.mark.parametrize(
    "value, expected", [("a", 0), ("b", 1), ("c", 2), ("d", 3), ("e", 4), ("f", 5), ("g", 6), ("h", 7)],
)
def test_to_int_lower(value, expected):
    assert utils.to_int(value) == expected


@pytest.mark.parametrize("value, expected", [(0, "A")])
def test_to_char(value, expected):
    assert utils.to_char(value) == expected
