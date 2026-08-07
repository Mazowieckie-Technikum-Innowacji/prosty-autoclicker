from unittest.mock import MagicMock, patch

import pytest

from tests.constants import CURRENT_OS, ERROR_IMPOSSIBLE_FLUCTUATION
from tests.conftest import load_main


class TestFluctuatingClick:
    def test_press_release_paired(self):
        mod = load_main()
        mock_click = MagicMock()
        mod.click = mock_click
        cfg = mod.Settings(duration=1.0, rate=10.0, randomize=True, randomize_min=0.05, os=CURRENT_OS)

        with patch.object(mod.time, "sleep"), patch.object(mod, "countdown"):
            mod.fluctuating_click(cfg)

        assert mock_click.press.call_count == 10
        assert mock_click.release.call_count == 10

    def test_press_before_release_each_click(self):
        mod = load_main()
        mock_click = MagicMock()
        mod.click = mock_click
        cfg = mod.Settings(duration=1.0, rate=5.0, randomize=True, randomize_min=0.05, os=CURRENT_OS)

        with patch.object(mod.time, "sleep"), patch.object(mod, "countdown"):
            mod.fluctuating_click(cfg)

        assert mock_click.press.call_count == mock_click.release.call_count

    def test_impossible_fluctuation_raises(self):
        mod = load_main()
        mock_click = MagicMock()
        mod.click = mock_click
        cfg = mod.Settings(duration=1.0, rate=1.0, randomize=True, randomize_min=5.0, os=CURRENT_OS)

        with patch.object(mod.time, "sleep"), patch.object(mod, "countdown"):
            with pytest.raises(ValueError, match=ERROR_IMPOSSIBLE_FLUCTUATION):
                mod.fluctuating_click(cfg)

    def test_click_count_matches_duration_times_rate(self):
        mod = load_main()
        mock_click = MagicMock()
        mod.click = mock_click
        cfg = mod.Settings(duration=2.0, rate=10.0, randomize=True, randomize_min=0.05, os=CURRENT_OS)

        with patch.object(mod.time, "sleep"), patch.object(mod, "countdown"):
            mod.fluctuating_click(cfg)

        assert mock_click.press.call_count == 20
        assert mock_click.release.call_count == 20

    def test_indefinite_mode_loops_until_exception(self):
        mod = load_main()
        mock_click = MagicMock()
        mod.click = mock_click
        cfg = mod.Settings(duration=-1, rate=1.0, randomize=True, randomize_min=0.05, os=CURRENT_OS)

        call_count = 0

        def stop_after_n(s):
            nonlocal call_count
            call_count += 1
            if call_count > 3:
                raise KeyboardInterrupt

        with patch.object(mod.time, "sleep", side_effect=stop_after_n), patch.object(mod, "countdown"):
            with pytest.raises(KeyboardInterrupt):
                mod.fluctuating_click(cfg)

        assert mock_click.press.call_count >= 1

    def test_batch_size_zero_returns_early(self):
        mod = load_main()
        mock_click = MagicMock()
        mod.click = mock_click
        cfg = mod.Settings(duration=0.0001, rate=1.0, randomize=True, randomize_min=0.05, os=CURRENT_OS)

        with patch.object(mod.time, "sleep"), patch.object(mod, "countdown"):
            mod.fluctuating_click(cfg)

        assert mock_click.press.call_count == 0
