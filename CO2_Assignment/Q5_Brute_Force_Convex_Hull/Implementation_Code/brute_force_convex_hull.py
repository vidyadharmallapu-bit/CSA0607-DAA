"""Supporting-line brute-force hull with collinear-edge extreme handling."""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2
from typing import Sequence


Point = tuple[float, float]


@dataclass(frozen=True)
class HullResult:
    vertices: list[Point]
    candidate_pairs: int
    orientation_tests: int


def orientation(first: Point, second: Point, point: Point) -> float:
    return ((second[0] - first[0]) * (point[1] - first[1])
            - (second[1] - first[1]) * (point[0] - first[0]))


def convex_hull(points: Sequence[Point]) -> HullResult:
    unique = list(dict.fromkeys(points))
    if len(unique) <= 1:
        return HullResult(unique, 0, 0)
    if len(unique) == 2:
        return HullResult(sorted(unique), 1, 0)

    candidate_pairs = 0
    orientation_tests = 0
    boundary_extremes: set[Point] = set()
    found_supporting_line = False
    for first_index in range(len(unique) - 1):
        for second_index in range(first_index + 1, len(unique)):
            first, second = unique[first_index], unique[second_index]
            candidate_pairs += 1
            positive = negative = False
            collinear = [first, second]
            for point_index, point in enumerate(unique):
                if point_index == first_index or point_index == second_index:
                    continue
                side = orientation(first, second, point)
                orientation_tests += 1
                if side > 0:
                    positive = True
                elif side < 0:
                    negative = True
                else:
                    collinear.append(point)
                if positive and negative:
                    break
            if positive and negative:
                continue
            found_supporting_line = True
            if first[0] != second[0]:
                endpoints = (min(collinear, key=lambda p: p[0]), max(collinear, key=lambda p: p[0]))
            else:
                endpoints = (min(collinear, key=lambda p: p[1]), max(collinear, key=lambda p: p[1]))
            boundary_extremes.update(endpoints)

    if not found_supporting_line:
        return HullResult([min(unique), max(unique)], candidate_pairs, orientation_tests)

    if len(boundary_extremes) <= 2:
        return HullResult(sorted(boundary_extremes), candidate_pairs, orientation_tests)
    center_x = sum(point[0] for point in boundary_extremes) / len(boundary_extremes)
    center_y = sum(point[1] for point in boundary_extremes) / len(boundary_extremes)
    ordered = sorted(boundary_extremes, key=lambda point: atan2(point[1] - center_y, point[0] - center_x))
    return HullResult(ordered, candidate_pairs, orientation_tests)


def main() -> None:
    points = [(0, 0), (2, 0), (4, 0), (4, 3), (0, 3), (2, 1), (0, 0)]
    result = convex_hull(points)
    print(f"input_points={len(points)} unique_points={len(set(points))} hull={result.vertices}")
    print(f"candidate_pairs={result.candidate_pairs} orientation_tests={result.orientation_tests}")


if __name__ == "__main__":
    main()