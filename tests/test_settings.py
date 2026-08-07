from unittest.mock import patch

from tests.constants import CURRENT_OS, TRUE_INPUT
from tests.conftest import load_main


def test_returns_settings_object():
    mod = load_main()
    mod.platform.system.return_value = CURRENT_OS
    with patch("builtins.input", side_effect=["2", "1", TRUE_INPUT, "0.1", TRUE_INPUT]):
        cfg = mod.get_settings()
    assert isinstance(cfg, mod.Settings)


def test_duration_zero_maps_to_indefinite():
    mod = load_main()
    mod.platform.system.return_value = CURRENT_OS
    with patch("builtins.input", side_effect=["0", "1", TRUE_INPUT, "0.1", TRUE_INPUT]):
        cfg = mod.get_settings()
    assert cfg.duration == -1


def test_os_detection():
    mod = load_main()
    mod.platform.system.return_value = CURRENT_OS
    with patch("builtins.input", side_effect=["2", "1", TRUE_INPUT, "0.1", TRUE_INPUT]):
        cfg = mod.get_settings()
    assert cfg.os == CURRENT_OS
