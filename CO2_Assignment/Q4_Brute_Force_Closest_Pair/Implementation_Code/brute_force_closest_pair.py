"""Quadratic closest-pair search using squared Euclidean distances."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Sequence


Point = tuple[float, float]


@dataclass(frozen=True)
class ClosestPairResult:
    first: Point
    second: Point
    distance: float
    pairs_examined: int
    distance_calculations: int


def closest_pair(points: Sequence[Point]) -> ClosestPairResult:
    if len(points) < 2:
        raise ValueError("at least two points are required")
    best_squared: float | None = None
    best_pair: tuple[Point, Point] | None = None
    pairs = 0
    for first_index in range(len(points) - 1):
        for second_index in range(first_index + 1, len(points)):
            first = points[first_index]
            second = points[second_index]
            dx = first[0] - second[0]
            dy = first[1] - second[1]
            squared = dx * dx + dy * dy
            pairs += 1
            if best_squared is None or squared < best_squared:
                best_squared = squared
                best_pair = (first, second)
    assert best_pair is not None and best_squared is not None
    return ClosestPairResult(*best_pair, sqrt(best_squared), pairs, pairs)


def main() -> None:
    points = [(0.0, 0.0), (2.0, 2.0), (3.0, 3.0), (8.0, 1.0)]
    result = closest_pair(points)
    print(f"points={len(points)} closest={result.first, result.second} distance={result.distance:.6f} pairs={result.pairs_examined} distance_calculations={result.distance_calculations}")


if __name__ == "__main__":
    main()