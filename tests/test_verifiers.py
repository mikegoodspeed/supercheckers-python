from unittest.mock import Mock, call, sentinel

import pytest

import supercheckers as sc
from supercheckers import verifiers


@pytest.fixture
def mock_all_rules():
    rule_1 = Mock(sc.Rule)
    rule_1.is_valid.return_value = True
    rule_2 = Mock(sc.Rule)
    rule_2.is_valid.return_value = False
    return [rule_1, rule_2]


@pytest.fixture
def verifier(mock_all_rules):
    return verifiers.Verifier(mock_all_rules)


@pytest.mark.parametrize("failed_rules, expected", [([], True), ([sentinel.rule_1], False)])
def test_result_is_valid(failed_rules, expected):
    assert verifiers.Result(failed_rules).is_valid is expected


def test_verifier_init(verifier, mock_all_rules):
    assert verifier.all_rules == mock_all_rules


def test_verifier_validate(verifier, mock_all_rules):
    rule_1, rule_2 = mock_all_rules
    result = verifier.verify(sentinel.journal, sentinel.move)
    assert isinstance(result, verifiers.Result)
    assert result.failed_rules == [rule_2]
    assert rule_1.mock_calls == [call.is_valid(sentinel.journal, sentinel.move)]
    assert rule_2.mock_calls == [call.is_valid(sentinel.journal, sentinel.move)]
