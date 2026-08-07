from unittest.mock import patch

import pytest

from tests.conftest import load_main
from tests.constants import CURRENT_OS, FALSE_INPUTS, SUPPORTED_OS_LIST, TRUE_INPUTS


def test_is_true():
    mod = load_main()
    for val in TRUE_INPUTS:
        assert mod.is_true(val) is True
    for val in FALSE_INPUTS:
        assert mod.is_true(val) is False
    assert mod.is_true("YES") is True


def test_is_supported_os():
    mod = load_main()
    for os_name in SUPPORTED_OS_LIST:
        assert mod.is_supported_os(os_name) is True
    assert mod.is_supported_os("macos") is False


def test_is_valid_number():
    mod = load_main()
    assert mod.is_valid_number("42") == 42.0
    assert mod.is_valid_number("3.14") == pytest.approx(3.14)
    assert mod.is_valid_number("abc") is False


def test_ask_number():
    mod = load_main()
    with patch("builtins.input", return_value="10"):
        result = mod.ask_number("Q: ", default=5.0, error="err")
        assert result == 10.0


def test_settings_dataclass():
    mod = load_main()
    s = mod.Settings(duration=2.0, rate=10.0, randomize=True, randomize_min=0.1, os=CURRENT_OS)
    assert s.duration == 2.0
    assert s.rate == 10.0
    assert s.randomize is True
