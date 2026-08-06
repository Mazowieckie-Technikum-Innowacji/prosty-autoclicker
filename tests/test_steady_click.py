from unittest.mock import MagicMock, patch

import pytest

from tests.conftest import load_main


class TestSteadyClick:
    def test_click_count_matches_duration_times_rate(self):
        mod = load_main()
        mock_click = MagicMock()
        mod.click = mock_click
        cfg = mod.Settings(duration=2.0, rate=10.0, randomize=False, randomize_min=0.0, os="linux")

        with patch.object(mod.time, "sleep"), patch.object(mod, "countdown"):
            mod.steady_click(cfg)

        assert mock_click.call_count == 20

    def test_countdown_called_before_clicking(self):
        mod = load_main()
        mock_click = MagicMock()
        mod.click = mock_click
        cfg = mod.Settings(duration=1.0, rate=5.0, randomize=False, randomize_min=0.0, os="linux")

        call_order = []
        with (
            patch.object(mod.time, "sleep"),
            patch.object(mod, "countdown", side_effect=lambda s: call_order.append("countdown")),
        ):
            mod.steady_click(cfg)

        assert call_order[0] == "countdown"

    def test_sleep_interval_is_one_over_rate(self):
        mod = load_main()
        mock_click = MagicMock()
        mod.click = mock_click
        cfg = mod.Settings(duration=1.0, rate=5.0, randomize=False, randomize_min=0.0, os="linux")

        with (
            patch.object(mod, "click", mock_click),
            patch.object(mod.time, "sleep") as mock_sleep,
            patch.object(mod, "countdown"),
        ):
            mod.steady_click(cfg)

        for call in mock_sleep.call_args_list:
            assert call.args[0] == pytest.approx(0.2)

    def test_indefinite_mode_requires_manual_stop(self):
        mod = load_main()
        mock_click = MagicMock()
        mod.click = mock_click
        cfg = mod.Settings(duration=-1, rate=1.0, randomize=False, randomize_min=0.0, os="linux")

        call_count = 0

        def stop_after_n(s):
            nonlocal call_count
            call_count += 1
            if call_count > 5:
                raise KeyboardInterrupt

        with patch.object(mod.time, "sleep", side_effect=stop_after_n), patch.object(mod, "countdown"):
            with pytest.raises(KeyboardInterrupt):
                mod.steady_click(cfg)

        assert mock_click.call_count == 5
