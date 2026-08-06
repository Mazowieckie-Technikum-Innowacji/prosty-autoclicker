import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest


class TestLinuxClick:
    @pytest.fixture
    def linux_click(self):
        mock_evdev = MagicMock()
        mock_ecodes = mock_evdev.ecodes
        mock_ecodes.EV_KEY = "EV_KEY"
        mock_ecodes.BTN_LEFT = "BTN_LEFT"
        mock_ecodes.BTN_RIGHT = "BTN_RIGHT"
        mock_ecodes.BTN_MIDDLE = "BTN_MIDDLE"

        sys.modules["evdev"] = mock_evdev
        try:
            if "click_platform.Linux" in sys.modules:
                del sys.modules["click_platform.Linux"]
            spec = importlib.util.spec_from_file_location(
                "click_platform.Linux",
                str(Path(__file__).resolve().parent.parent / "click_platform" / "Linux.py"),
            )
            mod = importlib.util.module_from_spec(spec)
            sys.modules["click_platform.Linux"] = mod
            spec.loader.exec_module(mod)
            click = mod.Click()
            return click, mock_evdev
        finally:
            del sys.modules["evdev"]
            if "click_platform.Linux" in sys.modules:
                del sys.modules["click_platform.Linux"]

    def test_press(self, linux_click):
        click, mock_evdev = linux_click
        click.press()
        mock_evdev.UInput.return_value.write.assert_any_call("EV_KEY", "BTN_LEFT", 1)
        mock_evdev.UInput.return_value.syn.assert_called()

    def test_release(self, linux_click):
        click, mock_evdev = linux_click
        click.release()
        mock_evdev.UInput.return_value.write.assert_any_call("EV_KEY", "BTN_LEFT", 0)
        mock_evdev.UInput.return_value.syn.assert_called()

    def test_call_does_press_and_release(self, linux_click):
        click, mock_evdev = linux_click
        mock_evdev.UInput.return_value.reset_mock()
        click()
        assert mock_evdev.UInput.return_value.write.call_count == 2
        assert mock_evdev.UInput.return_value.syn.call_count == 2


class TestWindowsClick:
    @pytest.fixture
    def windows_click(self):
        mock_pynput = MagicMock()
        mock_mouse = mock_pynput.mouse

        sys.modules["pynput"] = mock_pynput
        sys.modules["pynput.mouse"] = mock_mouse
        try:
            if "click_platform.Windows" in sys.modules:
                del sys.modules["click_platform.Windows"]
            spec = importlib.util.spec_from_file_location(
                "click_platform.Windows",
                str(Path(__file__).resolve().parent.parent / "click_platform" / "Windows.py"),
            )
            mod = importlib.util.module_from_spec(spec)
            sys.modules["click_platform.Windows"] = mod
            spec.loader.exec_module(mod)
            click = mod.Click()
            return click, mock_mouse
        finally:
            del sys.modules["pynput"]
            if "pynput.mouse" in sys.modules:
                del sys.modules["pynput.mouse"]
            if "click_platform.Windows" in sys.modules:
                del sys.modules["click_platform.Windows"]

    def test_press(self, windows_click):
        click, mock_mouse = windows_click
        ctrl = mock_mouse.Controller.return_value
        click.press()
        ctrl.press.assert_called_once_with(mock_mouse.Button.left)

    def test_release(self, windows_click):
        click, mock_mouse = windows_click
        ctrl = mock_mouse.Controller.return_value
        click.release()
        ctrl.release.assert_called_once_with(mock_mouse.Button.left)

    def test_call_does_press_and_release(self, windows_click):
        click, mock_mouse = windows_click
        ctrl = mock_mouse.Controller.return_value
        ctrl.reset_mock()
        click()
        assert ctrl.press.call_count == 1
        assert ctrl.release.call_count == 1
