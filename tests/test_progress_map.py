from __future__ import annotations

import io
from unittest.mock import patch

import pytest

from philiprehberger_progress_map import pmap


def double(x: int) -> int:
    return x * 2


def square(x: int) -> int:
    return x * x


def failing(x: int) -> int:
    raise ValueError(f"bad value: {x}")


class TestPmap:
    def test_results_match_serial_map(self) -> None:
        items = list(range(20))
        result = pmap(double, items, show_progress=False)
        assert result == [x * 2 for x in items]

    def test_empty_input_returns_empty_list(self) -> None:
        result = pmap(double, [], show_progress=False)
        assert result == []

    def test_single_item(self) -> None:
        result = pmap(double, [5], show_progress=False)
        assert result == [10]

    def test_preserves_order(self) -> None:
        items = list(range(50))
        result = pmap(square, items, show_progress=False)
        assert result == [x * x for x in items]

    def test_exception_propagates(self) -> None:
        with pytest.raises(ValueError, match="bad value"):
            pmap(failing, [1, 2, 3], show_progress=False)

    def test_show_progress_false_suppresses_output(self) -> None:
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            pmap(double, [1, 2, 3], show_progress=False)
        assert stderr.getvalue() == ""

    def test_label_appears_in_output(self) -> None:
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            pmap(double, [1, 2, 3], label="Testing", show_progress=True)
        output = stderr.getvalue()
        assert "Testing" in output

    def test_workers_parameter_accepted(self) -> None:
        result = pmap(double, [1, 2, 3, 4], workers=2, show_progress=False)
        assert result == [2, 4, 6, 8]

    def test_works_with_lambda(self) -> None:
        result = pmap(lambda x: x + 10, [1, 2, 3], show_progress=False)
        assert result == [11, 12, 13]

    def test_progress_bar_shows_completion(self) -> None:
        stderr = io.StringIO()
        with patch("sys.stderr", stderr):
            pmap(double, [1, 2, 3], show_progress=True)
        output = stderr.getvalue()
        assert "3/3" in output
        assert "100%" in output
