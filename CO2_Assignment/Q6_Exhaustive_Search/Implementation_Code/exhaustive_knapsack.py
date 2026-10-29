"""Exhaustive 0/1 knapsack by visiting every subset bitmask."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Package:
    package_id: str
    weight: int
    value: int


@dataclass(frozen=True)
class KnapsackResult:
    package_ids: tuple[str, ...]
    total_weight: int
    total_value: int
    subsets_examined: int
    feasible_subsets: int


def _is_better(value: int, weight: int, ids: tuple[str, ...], best: tuple[int, int, tuple[str, ...]]) -> bool:
    best_value, best_weight, best_ids = best
    return value > best_value or (value == best_value and (weight < best_weight or (weight == best_weight and ids < best_ids)))


def exhaustive_knapsack(packages: Sequence[Package], capacity: int) -> KnapsackResult:
    if capacity < 0:
        raise ValueError("capacity must be nonnegative")
    if len({item.package_id for item in packages}) != len(packages):
        raise ValueError("package IDs must be unique")
    if any(item.weight <= 0 or item.value < 0 for item in packages):
        raise ValueError("weights must be positive and values nonnegative")

    best = (0, 0, tuple())
    best_ids: tuple[str, ...] = tuple()
    best_weight = 0
    feasible = 0
    for mask in range(1 << len(packages)):
        weight = value = 0
        selected: list[str] = []
        for index, item in enumerate(packages):
            if mask & (1 << index):
                weight += item.weight
                value += item.value
                selected.append(item.package_id)
        if weight <= capacity:
            feasible += 1
            ids = tuple(sorted(selected))
            if _is_better(value, weight, ids, best):
                best = (value, weight, ids)
                best_ids = ids
                best_weight = weight
    return KnapsackResult(best_ids, best_weight, best[0], 1 << len(packages), feasible)


def main() -> None:
    packages = [Package("MED", 2, 8), Package("WATER", 3, 10), Package("FOOD", 4, 12), Package("RADIO", 1, 4)]
    result = exhaustive_knapsack(packages, 6)
    print(f"capacity=6 packages={len(packages)} selected={result.package_ids} weight={result.total_weight} value={result.total_value}")
    print(f"subsets_examined={result.subsets_examined} feasible_subsets={result.feasible_subsets}")


if __name__ == "__main__":
    main()