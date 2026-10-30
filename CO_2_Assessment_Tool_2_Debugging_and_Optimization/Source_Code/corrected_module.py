"""Minimally corrected versions of the supplied SentinelOps algorithms."""

from __future__ import annotations

from math import hypot, inf
from typing import TypeAlias

Alert: TypeAlias = tuple[str, int]
Point: TypeAlias = tuple[float, float]


def sort_alerts(alerts: list[Alert]) -> list[Alert]:
    """Stable in-place insertion sort by descending severity."""
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j >= 0 and alerts[j][1] < key[1]:
            alerts[j + 1] = alerts[j]
            j -= 1
        alerts[j + 1] = key
    return alerts


def is_blocked(blocklist: list[str], ip: str) -> bool:
    """Return True exactly when ip occurs in the blocklist."""
    for i in range(len(blocklist)):
        if blocklist[i] == ip:
            return True
    return False


def find_signature(log: str, pattern: str) -> list[int]:
    """Return all zero-based matches, including overlaps.

    An empty pattern matches all n+1 boundaries of a string of length n.
    """
    n, m = len(log), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    hits: list[int] = []
    for i in range(n - m + 1):
        j = 0
        while j < m and log[i + j] == pattern[j]:
            j += 1
        if j == m:
            hits.append(i)
    return hits


def closest_logins(events: list[Point]) -> tuple[tuple[int, int], float]:
    """Return the minimum-distance pair, breaking ties by index pair."""
    if len(events) < 2:
        raise ValueError("at least two login events are required")
    best_squared = inf
    best_pair: tuple[int, int] | None = None
    for i in range(len(events) - 1):
        for j in range(i + 1, len(events)):
            dx = events[i][0] - events[j][0]
            dy = events[i][1] - events[j][1]
            squared = dx * dx + dy * dy
            candidate = (i, j)
            if squared < best_squared or (squared == best_squared and (best_pair is None or candidate < best_pair)):
                best_squared = squared
                best_pair = candidate
    assert best_pair is not None
    return best_pair, hypot(events[best_pair[0]][0] - events[best_pair[1]][0], events[best_pair[0]][1] - events[best_pair[1]][1])
