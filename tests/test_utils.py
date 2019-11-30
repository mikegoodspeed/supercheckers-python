import pytest

import supercheckers as sc
from supercheckers import utils


@pytest.mark.parametrize("row_id", [0, 1, 2, 3, 4, 5, 6, 7, 8])
@pytest.mark.parametrize("col_id", [0, 1, 2, 3, 4, 5, 6, 7, 8])
def test_compare_identical(row_id, col_id):
    loc = (row_id, col_id)
    result = utils.compare(loc, loc)
    assert result == utils.Description(sc.Direction.IDENTICAL, 0)


@pytest.mark.parametrize(
    "src_loc, dst_loc",
    [
        ((0, 0), (0, 3)),
        ((1, 1), (1, 2)),
        ((2, 2), (2, 7)),
        ((3, 3), (3, 6)),
        ((4, 4), (4, 5)),
        ((5, 5), (5, 6)),
        ((6, 6), (6, 7)),
        ((7, 6), (7, 7)),
    ],
)
def test_compare_east(src_loc, dst_loc):
    result = utils.compare(src_loc, dst_loc)
    assert result == utils.Description(sc.Direction.EAST, dst_loc[1] - src_loc[1])


@pytest.mark.parametrize(
    "src_loc, dst_loc",
    [
        ((0, 3), (0, 0)),
        ((1, 2), (1, 1)),
        ((2, 7), (2, 2)),
        ((3, 6), (3, 3)),
        ((4, 5), (4, 4)),
        ((5, 6), (5, 5)),
        ((6, 7), (6, 6)),
        ((7, 7), (7, 6)),
    ],
)
def test_compare_west(src_loc, dst_loc):
    result = utils.compare(src_loc, dst_loc)
    assert result == utils.Description(sc.Direction.WEST, dst_loc[1] - src_loc[1])


@pytest.mark.parametrize(
    "src_loc, dst_loc",
    [
        ((0, 0), (3, 0)),
        ((1, 1), (2, 1)),
        ((2, 2), (7, 2)),
        ((3, 3), (6, 3)),
        ((4, 4), (5, 4)),
        ((5, 5), (6, 5)),
        ((6, 6), (7, 6)),
        ((6, 7), (7, 7)),
    ],
)
def test_compare_north(src_loc, dst_loc):
    result = utils.compare(src_loc, dst_loc)
    assert result == utils.Description(sc.Direction.NORTH, dst_loc[0] - src_loc[0])


@pytest.mark.parametrize(
    "src_loc, dst_loc",
    [
        ((3, 0), (0, 0)),
        ((2, 1), (1, 1)),
        ((7, 2), (2, 2)),
        ((6, 3), (3, 3)),
        ((5, 4), (4, 4)),
        ((6, 5), (5, 5)),
        ((7, 6), (6, 6)),
        ((7, 7), (6, 7)),
    ],
)
def test_compare_south(src_loc, dst_loc):
    result = utils.compare(src_loc, dst_loc)
    assert result == utils.Description(sc.Direction.SOUTH, dst_loc[0] - src_loc[0])


@pytest.mark.parametrize(
    "src_loc, dst_loc",
    [
        ((0, 0), (1, 3)),
        ((1, 1), (2, 2)),
        ((2, 2), (3, 7)),
        ((3, 3), (4, 6)),
        ((4, 4), (3, 5)),
        ((5, 5), (2, 6)),
        ((6, 6), (1, 7)),
        ((7, 6), (0, 7)),
    ],
)
def test_compare_unknown(src_loc, dst_loc):
    result = utils.compare(src_loc, dst_loc)
    assert result == utils.Description(sc.Direction.UNKNOWN, None)


@pytest.mark.parametrize("row_id", [0, 1, 2, 3, 4, 5, 6, 7, 8])
@pytest.mark.parametrize("col_id", [0, 1, 2, 3, 4, 5, 6, 7, 8])
def test_in_middle(row_id, col_id):
    expected = (2 <= row_id <= 5) and (2 <= col_id <= 5)
    assert utils.in_middle(row_id, col_id) is expected


@pytest.mark.parametrize("row_id", [0, 1, 2, 3, 4, 5, 6, 7, 8])
@pytest.mark.parametrize("col_id", [0, 1, 2, 3, 4, 5, 6, 7, 8])
def test_in_middle_extended(row_id, col_id):
    expected = (2 <= row_id <= 5) and (1 <= col_id <= 5)
    assert utils.in_middle(row_id, col_id, extended=True) is expected


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
