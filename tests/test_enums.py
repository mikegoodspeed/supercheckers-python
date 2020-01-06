import pytest

from supercheckers import enums


@pytest.mark.parametrize(
    "value, expected",
    [
        (-1, enums.MoveType.UNKNOWN),
        (0, enums.MoveType.UNKNOWN),
        (1, enums.MoveType.SLIDE),
        (2, enums.MoveType.JUMP),
        (3, enums.MoveType.UNKNOWN),
    ],
)
def test_move_type_from_distance(value, expected):
    assert enums.MoveType.from_distance(value) == expected
