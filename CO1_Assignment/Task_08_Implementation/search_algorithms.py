"""Search strategies for unique student registration numbers."""

from typing import Mapping, Optional, Sequence


def linear_search(records: Sequence[str], target: str) -> Optional[str]:
    """Return the matching registration number, or None if it is absent."""
    for registration_number in records:
        if registration_number == target:
            return registration_number
    return None


def recursive_binary_search(
    sorted_records: Sequence[str],
    target: str,
    low: int = 0,
    high: Optional[int] = None,
) -> Optional[str]:
    """Search an ascending sequence recursively; the input must be sorted."""
    if high is None:
        high = len(sorted_records) - 1
    if low > high:
        return None

    middle = (low + high) // 2
    candidate = sorted_records[middle]
    if candidate == target:
        return candidate
    if target < candidate:
        return recursive_binary_search(sorted_records, target, low, middle - 1)
    return recursive_binary_search(sorted_records, target, middle + 1, high)


def hash_search(index: Mapping[str, str], target: str) -> Optional[str]:
    """Return the indexed registration number, or None if it is absent."""
    return index.get(target)
