from unittest.mock import patch

from tests.conftest import load_main


def test_returns_settings_object():
    mod = load_main()
    mod.platform.system.return_value = "Linux"
    with patch("builtins.input", side_effect=["2", "1", "t", "0.1", "t"]):
        cfg = mod.get_settings()
    assert isinstance(cfg, mod.Settings)


def test_duration_zero_maps_to_indefinite():
    mod = load_main()
    mod.platform.system.return_value = "Linux"
    with patch("builtins.input", side_effect=["0", "1", "t", "0.1", "t"]):
        cfg = mod.get_settings()
    assert cfg.duration == -1


def test_os_detection_linux():
    mod = load_main()
    mod.platform.system.return_value = "Linux"
    with patch("builtins.input", side_effect=["2", "1", "t", "0.1", "t"]):
        cfg = mod.get_settings()
    assert cfg.os == "linux"
