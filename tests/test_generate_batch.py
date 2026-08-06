import numpy as np
import pytest

from tests.conftest import load_main


class TestGenerateBatch:
    @pytest.fixture
    def gen(self):
        return load_main().generate_batch

    def test_returns_tuple_of_arrays(self, gen):
        sleeps, holds = gen(10, 0.05, 0.15, 0.1)
        assert isinstance(sleeps, np.ndarray)
        assert isinstance(holds, np.ndarray)

    def test_array_lengths_match_batch_size(self, gen):
        for size in [1, 5, 50, 500]:
            sleeps, holds = gen(size, 0.05, 0.15, 0.1)
            assert len(sleeps) == size
            assert len(holds) == size

    def test_all_values_non_negative(self, gen):
        sleeps, holds = gen(100, 0.05, 0.15, 0.1)
        assert np.all(sleeps >= 0)
        assert np.all(holds >= 0)

    def test_holds_in_range(self, gen):
        _, holds = gen(1000, 0.05, 0.15, 0.1)
        assert np.all(holds >= 0.002)
        assert np.all(holds <= 0.015)

    def test_sleeps_clipped_to_bounds(self, gen):
        sleeps, _ = gen(500, 0.08, 0.12, 0.1)
        assert np.all(sleeps >= 0.0)
        assert np.all(sleeps <= 0.12 + 0.06)

    def test_sleep_sum_approximates_target(self, gen):
        batch_size = 100
        target_sleep = 0.1
        sleeps, _holds = gen(batch_size, 0.05, 0.15, target_sleep)
        expected_total = batch_size * target_sleep
        assert sleeps.sum() == pytest.approx(expected_total, rel=0.3)

    def test_batch_size_zero(self, gen):
        sleeps, holds = gen(0, 0.05, 0.15, 0.1)
        assert len(sleeps) == 0
        assert len(holds) == 0

    def test_min_equals_max(self, gen):
        sleeps, _holds = gen(50, 0.1, 0.1, 0.1)
        assert np.all(sleeps >= 0)

    def test_target_sleep_zero(self, gen):
        sleeps, _holds = gen(50, 0.05, 0.15, 0.0)
        assert np.all(sleeps >= 0)

    def test_deterministic_with_seed(self, gen):
        np.random.seed(42)
        s1, h1 = gen(20, 0.05, 0.15, 0.1)
        np.random.seed(42)
        s2, h2 = gen(20, 0.05, 0.15, 0.1)
        np.testing.assert_array_equal(s1, s2)
        np.testing.assert_array_equal(h1, h2)

    def test_jump_mask_injection(self, gen):
        np.random.seed(0)
        sleeps, _ = gen(1000, 0.05, 0.15, 0.1)
        min_sleep = 0.05
        max_sleep = 0.15
        in_range = np.sum((sleeps >= min_sleep) & (sleeps <= max_sleep))
        at_bounds = np.sum((sleeps == min_sleep) | (sleeps == max_sleep))
        assert in_range + at_bounds >= 900
