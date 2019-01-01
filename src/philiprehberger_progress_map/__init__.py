"""Parallel map with a built-in terminal progress bar."""

from __future__ import annotations

import sys
from collections.abc import Callable, Iterable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import TypeVar

__all__ = ["pmap"]

T = TypeVar("T")
R = TypeVar("R")


def pmap(
    func: Callable[[T], R],
    items: Iterable[T],
    *,
    workers: int = 4,
    mp: bool = False,
    label: str = "",
    show_progress: bool = True,
) -> list[R]:
    """Apply func to each item in parallel with a progress bar.

    Args:
        func: Function to apply to each item.
        items: Iterable of items to process.
        workers: Number of worker threads or processes.
        mp: Use multiprocessing instead of threading.
        label: Optional label prefix for the progress bar.
        show_progress: Whether to display the progress bar.
    """
    item_list = list(items)
    total = len(item_list)

    if total == 0:
        return []

    executor_cls = ProcessPoolExecutor if mp else ThreadPoolExecutor
    results: list[R | None] = [None] * total

    with executor_cls(max_workers=workers) as executor:
        future_to_index = {
            executor.submit(func, item): i for i, item in enumerate(item_list)
        }

        completed = 0
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            results[idx] = future.result()
            completed += 1
            if show_progress:
                _print_progress(completed, total, label)

    if show_progress:
        sys.stderr.write("\n")

    return results  # type: ignore[return-value]


def _print_progress(current: int, total: int, label: str) -> None:
    """Print a carriage-return progress bar to stderr."""
    width = 30
    filled = int(width * current / total)
    bar = "\u2588" * filled + "\u2591" * (width - filled)
    pct = current / total * 100
    prefix = f"{label} " if label else ""
    sys.stderr.write(f"\r{prefix}|{bar}| {current}/{total} ({pct:.0f}%)")
    sys.stderr.flush()
