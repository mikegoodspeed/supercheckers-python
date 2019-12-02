from unittest.mock import sentinel

import pytest

import supercheckers as sc
from supercheckers import moves


@pytest.mark.parametrize("locations", [[], [sentinel.loc_1], [sentinel.loc_1, sentinel.loc_2]])
def test_move_len(locations):
    move = moves.Move(sentinel.team, locations)
    assert len(move) == len(locations)


@pytest.mark.parametrize(
    "team, locations, expected",
    [
        (sc.Team.ONE, [], "[X: ]"),
        (sc.Team.TWO, [(0, 0)], "[O: A1]"),
        (sc.Team.ONE, [(7, 7), (5, 5)], "[X: H8 F6]"),
        (sc.Team.TWO, [(1, 2), (2, 2)], "[O: C2 C3]"),
    ],
)
def test_move_str(team, locations, expected):
    move = moves.Move(team, locations)
    assert str(move) == expected
