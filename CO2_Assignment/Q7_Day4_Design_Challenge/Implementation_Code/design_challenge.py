"""Branch-and-bound exact knapsack with fractional relaxation upper bound."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Sequence

from CO2_Assignment.Q6_Exhaustive_Search.Implementation_Code.exhaustive_knapsack import (
    Package,
    _is_better,
)


@dataclass(frozen=True)
class BranchBoundResult:
    package_ids: tuple[str, ...]
    total_weight: int
    total_value: int
    visited_nodes: int
    expanded_nodes: int
    pruned_nodes: int
    complete_subsets_evaluated: int
    preprocessing_seconds: float
    search_seconds: float


def branch_and_bound_knapsack(packages: Sequence[Package], capacity: int) -> BranchBoundResult:
    if capacity < 0:
        raise ValueError("capacity must be nonnegative")
    if len({item.package_id for item in packages}) != len(packages):
        raise ValueError("package IDs must be unique")
    if any(item.weight <= 0 or item.value < 0 for item in packages):
        raise ValueError("weights must be positive and values nonnegative")

    preprocessing_start = perf_counter()
    indexed = sorted(enumerate(packages), key=lambda pair: (-pair[1].value / pair[1].weight, pair[1].package_id))
    ordered = [item for _, item in indexed]
    original_indices = [index for index, _ in indexed]
    preprocessing_seconds = perf_counter() - preprocessing_start

    def upper_bound(index: int, weight: int, value: int) -> float:
        remaining_capacity = capacity - weight
        bound = float(value)
        for item in ordered[index:]:
            if item.weight <= remaining_capacity:
                remaining_capacity -= item.weight
                bound += item.value
            else:
                bound += item.value * remaining_capacity / item.weight
                break
        return bound

    best = (0, 0, tuple())
    best_mask = 0
    visited = expanded = pruned = complete_subsets = 0
    search_start = perf_counter()

    def visit(index: int, weight: int, value: int, mask: int) -> None:
        nonlocal best, best_mask, visited, expanded, pruned, complete_subsets
        visited += 1
        if weight > capacity:
            pruned += 1
            return
        if index == len(ordered):
            complete_subsets += 1
            ids = tuple(sorted(packages[i].package_id for i in range(len(packages)) if mask & (1 << i)))
            if _is_better(value, weight, ids, best):
                best = (value, weight, ids)
                best_mask = mask
            return
        if upper_bound(index, weight, value) < best[0]:
            pruned += 1
            return
        expanded += 1
        original_index = original_indices[index]
        item = ordered[index]
        visit(index + 1, weight + item.weight, value + item.value, mask | (1 << original_index))
        visit(index + 1, weight, value, mask)

    visit(0, 0, 0, 0)
    search_seconds = perf_counter() - search_start
    ids = tuple(sorted(packages[index].package_id for index in range(len(packages)) if best_mask & (1 << index)))
    return BranchBoundResult(ids, best[1], best[0], visited, expanded, pruned, complete_subsets, preprocessing_seconds, search_seconds)


def main() -> None:
    packages = [Package("MED", 2, 8), Package("WATER", 3, 10), Package("FOOD", 4, 12), Package("RADIO", 1, 4)]
    result = branch_and_bound_knapsack(packages, 6)
    print(f"capacity=6 packages={len(packages)} selected={result.package_ids} weight={result.total_weight} value={result.total_value}")
    print(f"visited_nodes={result.visited_nodes} expanded_nodes={result.expanded_nodes} pruned_nodes={result.pruned_nodes}")
    print(f"preprocessing_seconds={result.preprocessing_seconds:.9f} search_seconds={result.search_seconds:.9f}")


if __name__ == "__main__":
    main()