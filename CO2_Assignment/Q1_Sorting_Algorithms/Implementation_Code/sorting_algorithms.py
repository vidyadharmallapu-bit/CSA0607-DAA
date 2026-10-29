"""Instrumented elementary sorting algorithms used in the CO2 experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class SortStats:
    comparisons: int
    movements: int
    swaps: int


def selection_sort(values: list[int]) -> SortStats:
    comparisons = movements = swaps = 0
    for start in range(len(values) - 1):
        minimum = start
        for index in range(start + 1, len(values)):
            comparisons += 1
            if values[index] < values[minimum]:
                minimum = index
        if minimum != start:
            values[start], values[minimum] = values[minimum], values[start]
            movements += 3
            swaps += 1
    return SortStats(comparisons, movements, swaps)


def bubble_sort(values: list[int]) -> SortStats:
    comparisons = movements = swaps = 0
    for end in range(len(values) - 1, 0, -1):
        changed = False
        for index in range(end):
            comparisons += 1
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]
                movements += 3
                swaps += 1
                changed = True
        if not changed:
            break
    return SortStats(comparisons, movements, swaps)


def insertion_sort(values: list[int]) -> SortStats:
    comparisons = movements = 0
    for index in range(1, len(values)):
        item = values[index]
        cursor = index - 1
        while cursor >= 0:
            comparisons += 1
            if values[cursor] <= item:
                break
            values[cursor + 1] = values[cursor]
            movements += 1
            cursor -= 1
        values[cursor + 1] = item
        movements += 1
    return SortStats(comparisons, movements, 0)


SORTS: dict[str, Callable[[list[int]], SortStats]] = {
    "selection": selection_sort,
    "bubble_early_exit": bubble_sort,
    "insertion": insertion_sort,
}


def main() -> None:
    from time import perf_counter

    datasets = {
        "reverse": list(range(20, 0, -1)),
        "nearly_sorted": list(range(1, 20)) + [0],
        "empty": [],
    }
    for dataset_name, source in datasets.items():
        print(f"dataset={dataset_name} n={len(source)} input={source}")
        for name, algorithm in SORTS.items():
            values = source.copy()
            start = perf_counter()
            stats = algorithm(values)
            elapsed = perf_counter() - start
            print(f"  {name}: sorted={values == sorted(source)} comparisons={stats.comparisons} movements={stats.movements} swaps={stats.swaps} seconds={elapsed:.9f}")


if __name__ == "__main__":
    main()