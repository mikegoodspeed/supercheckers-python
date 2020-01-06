from unittest.mock import MagicMock, Mock

import pytest

import supercheckers as sc
from supercheckers import games


@pytest.fixture
def mock_player_1() -> Mock:
    return Mock(sc.Player)


@pytest.fixture
def mock_player_2() -> Mock:
    return Mock(sc.Player)


@pytest.fixture
def mock_journal() -> MagicMock:
    return MagicMock(sc.Journal)


@pytest.fixture
def game_state(mock_player_1, mock_player_2, mock_journal) -> games.GameState:
    return games.GameState(mock_player_1, mock_player_2, mock_journal)


@pytest.mark.parametrize("turn_number", [0, 1, 2])
def test_games_current_player(game_state, mock_journal, turn_number):
    mock_journal.current_turn_number = turn_number
    expected = game_state.player_1 if turn_number % 2 != 0 else game_state.player_2
    assert game_state.current_player == expected


def test_games_current_player_starts(game_state, mock_player_1):
    assert game_state.current_player == mock_player_1
