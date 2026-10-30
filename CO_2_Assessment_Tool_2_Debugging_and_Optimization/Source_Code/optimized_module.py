"""Instrumented optimisations preserving the corrected public results."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot, inf, sqrt
from CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code.corrected_module import Alert, Point


@dataclass(frozen=True)
class OperationCounts:
    comparisons: int
    movements: int


@dataclass(frozen=True)
class SearchCounts:
    index_build_operations: int
    lookups: int


@dataclass(frozen=True)
class MatchResult:
    positions: list[int]
    character_comparisons: int


@dataclass(frozen=True)
class ClosestPairResult:
    pair: tuple[int, int]
    distance: float
    candidate_pairs: int
    distance_calculations: int
    preprocessing_operations: int


def insertion_sort_alerts_instrumented(alerts: list[Alert]) -> OperationCounts:
    """Stable insertion sort; movements count writes into the alert array."""
    comparisons = movements = 0
    for index in range(1, len(alerts)):
        key = alerts[index]
        cursor = index - 1
        while cursor >= 0:
            comparisons += 1
            if alerts[cursor][1] >= key[1]:
                break
            alerts[cursor + 1] = alerts[cursor]
            movements += 1
            cursor -= 1
        alerts[cursor + 1] = key
        movements += 1
    return OperationCounts(comparisons, movements)


def insertion_sort_alerts(alerts: list[Alert]) -> list[Alert]:
    """Compatible in-place insertion sort returning the sorted alert list."""
    insertion_sort_alerts_instrumented(alerts)
    return alerts


def stable_merge_sort_alerts_instrumented(alerts: list[Alert]) -> OperationCounts:
    """Stable O(n log n) descending alternative, sorting alerts in place."""
    comparisons = movements = 0
    buffer: list[Alert | None] = [None] * len(alerts)
    width = 1
    while width < len(alerts):
        start = 0
        while start < len(alerts):
            middle = min(start + width, len(alerts))
            end = min(start + 2 * width, len(alerts))
            left, right, output = start, middle, start
            while left < middle and right < end:
                comparisons += 1
                if alerts[left][1] >= alerts[right][1]:
                    buffer[output] = alerts[left]
                    left += 1
                else:
                    buffer[output] = alerts[right]
                    right += 1
                output += 1
                movements += 1
            while left < middle:
                buffer[output] = alerts[left]
                left += 1
                output += 1
                movements += 1
            while right < end:
                buffer[output] = alerts[right]
                right += 1
                output += 1
                movements += 1
            for position in range(start, end):
                item = buffer[position]
                assert item is not None
                alerts[position] = item
                movements += 1
            start += 2 * width
        width *= 2
    return OperationCounts(comparisons, movements)


def stable_merge_sort_alerts(alerts: list[Alert]) -> list[Alert]:
    """Compatible in-place stable merge sort returning the sorted alert list."""
    stable_merge_sort_alerts_instrumented(alerts)
    return alerts


class BlocklistIndex:
    """Reusable set index for many membership queries."""

    def __init__(self, blocklist: list[str]) -> None:
        self._blocked = set(blocklist)
        self.build_operations = len(blocklist)

    def is_blocked(self, ip: str) -> bool:
        return ip in self._blocked

    def query_many(self, queries: list[str]) -> tuple[list[bool], SearchCounts]:
        return [self.is_blocked(query) for query in queries], SearchCounts(self.build_operations, len(queries))


def find_signature_instrumented(log: str, pattern: str) -> MatchResult:
    """Counted brute-force matching with early mismatch exit and overlaps."""
    n, m = len(log), len(pattern)
    if m == 0:
        return MatchResult(list(range(n + 1)), 0)
    if m > n:
        return MatchResult([], 0)
    positions: list[int] = []
    comparisons = 0
    for start in range(n - m + 1):
        offset = 0
        while offset < m:
            comparisons += 1
            if log[start + offset] != pattern[offset]:
                break
            offset += 1
        if offset == m:
            positions.append(start)
    return MatchResult(positions, comparisons)


def find_signature(log: str, pattern: str) -> list[int]:
    """Compatible signature API returning only zero-based match positions."""
    return find_signature_instrumented(log, pattern).positions


def closest_logins_brute_force_instrumented(events: list[Point]) -> ClosestPairResult:
    """Exact unique-pair baseline using squared distances and index tie-break."""
    if len(events) < 2:
        raise ValueError("at least two login events are required")
    best_squared = inf
    best_pair: tuple[int, int] | None = None
    candidates = 0
    for first in range(len(events) - 1):
        for second in range(first + 1, len(events)):
            dx = events[first][0] - events[second][0]
            dy = events[first][1] - events[second][1]
            squared = dx * dx + dy * dy
            candidates += 1
            pair = (first, second)
            if squared < best_squared or (squared == best_squared and (best_pair is None or pair < best_pair)):
                best_squared, best_pair = squared, pair
    assert best_pair is not None
    return ClosestPairResult(best_pair, sqrt(best_squared), candidates, candidates, 0)


def closest_logins_brute_force(events: list[Point]) -> tuple[tuple[int, int], float]:
    """Compatible brute-force baseline returning pair and distance."""
    result = closest_logins_brute_force_instrumented(events)
    return result.pair, result.distance


def closest_logins_instrumented(events: list[Point]) -> ClosestPairResult:
    """Exact divide-and-conquer closest pair with a bounded seven-point strip.

    Duplicate coordinates are detected first and return the lexicographically
    earliest zero-distance pair. Otherwise all points are distinct, so the
    recursive minimum distance is positive and the standard strip packing bound
    limits checks to the next seven y-ordered points.
    """
    count = len(events)
    if count < 2:
        raise ValueError("at least two login events are required")

    coordinate_indices: dict[Point, list[int]] = {}
    preprocessing_operations = 0
    for index, point in enumerate(events):
        if len(point) != 2:
            raise ValueError("each event must contain exactly two coordinates")
        coordinate_indices.setdefault((point[0], point[1]), []).append(index)
        preprocessing_operations += 1
    duplicate_pairs = [
        (indices[0], indices[1])
        for indices in coordinate_indices.values()
        if len(indices) > 1
    ]
    if duplicate_pairs:
        return ClosestPairResult(min(duplicate_pairs), 0.0, 0, 0, preprocessing_operations)

    points_x = sorted((point[0], point[1], index) for index, point in enumerate(events))
    preprocessing_operations += count
    # Each recursive call returns the same subproblem sorted by y.
    candidate_pairs = 0
    distance_calculations = 0

    def squared_distance(first: tuple[float, float, int], second: tuple[float, float, int]) -> float:
        nonlocal candidate_pairs, distance_calculations
        candidate_pairs += 1
        distance_calculations += 1
        dx = first[0] - second[0]
        dy = first[1] - second[1]
        return dx * dx + dy * dy

    def better(
        current: tuple[float, tuple[int, int]] | None,
        candidate_squared: float,
        first_index: int,
        second_index: int,
    ) -> tuple[float, tuple[int, int]]:
        pair = tuple(sorted((first_index, second_index)))
        if current is None or candidate_squared < current[0] or (candidate_squared == current[0] and pair < current[1]):
            return candidate_squared, pair
        return current

    def solve(
        x_order: list[tuple[float, float, int]],
        y_order: list[tuple[float, float, int]],
    ) -> tuple[tuple[float, tuple[int, int]], list[tuple[float, float, int]]]:
        nonlocal preprocessing_operations
        size = len(x_order)
        if size <= 3:
            best: tuple[float, tuple[int, int]] | None = None
            for first in range(size - 1):
                for second in range(first + 1, size):
                    first_point, second_point = x_order[first], x_order[second]
                    best = better(best, squared_distance(first_point, second_point), first_point[2], second_point[2])
            assert best is not None
            return best, sorted(x_order, key=lambda point: (point[1], point[0], point[2]))

        middle = size // 2
        left_x, right_x = x_order[:middle], x_order[middle:]
        left_ids = {point[2] for point in left_x}
        left_y: list[tuple[float, float, int]] = []
        right_y: list[tuple[float, float, int]] = []
        for point in y_order:
            preprocessing_operations += 1
            (left_y if point[2] in left_ids else right_y).append(point)
        left_best, left_y = solve(left_x, left_y)
        right_best, right_y = solve(right_x, right_y)
        best = left_best if left_best[0] < right_best[0] or (left_best[0] == right_best[0] and left_best[1] < right_best[1]) else right_best

        merged_y: list[tuple[float, float, int]] = []
        left_cursor = right_cursor = 0
        while left_cursor < len(left_y) and right_cursor < len(right_y):
            preprocessing_operations += 1
            if (left_y[left_cursor][1], left_y[left_cursor][0], left_y[left_cursor][2]) <= (right_y[right_cursor][1], right_y[right_cursor][0], right_y[right_cursor][2]):
                merged_y.append(left_y[left_cursor])
                left_cursor += 1
            else:
                merged_y.append(right_y[right_cursor])
                right_cursor += 1
        merged_y.extend(left_y[left_cursor:])
        merged_y.extend(right_y[right_cursor:])
        split_x = right_x[0][0]
        strip: list[tuple[float, float, int]] = []
        for point in merged_y:
            preprocessing_operations += 1
            if (point[0] - split_x) ** 2 <= best[0]:
                strip.append(point)
        for first in range(len(strip)):
            limit = min(first + 8, len(strip))
            second = first + 1
            while second < limit:
                if (strip[first][2] in left_ids) == (strip[second][2] in left_ids):
                    second += 1
                    continue
                dy = strip[second][1] - strip[first][1]
                if dy * dy > best[0]:
                    break
                distance_squared = squared_distance(strip[first], strip[second])
                best = better(best, distance_squared, strip[first][2], strip[second][2])
                second += 1
        return best, merged_y

    initial_y = sorted(points_x, key=lambda point: (point[1], point[0], point[2]))
    best, _ = solve(points_x, initial_y)
    return ClosestPairResult(best[1], sqrt(best[0]), candidate_pairs, distance_calculations, preprocessing_operations)


def closest_logins(events: list[Point]) -> tuple[tuple[int, int], float]:
    """Compatible optimized API returning the corrected public result."""
    result = closest_logins_instrumented(events)
    return result.pair, result.distance
