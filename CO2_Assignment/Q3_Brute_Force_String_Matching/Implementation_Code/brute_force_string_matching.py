"""Straightforward all-occurrences string matcher with explicit comparisons."""

from __future__ import annotations


def brute_force_match(text: str, pattern: str) -> tuple[list[int], int]:
    """Return zero-based match starts and character comparisons.

    The empty pattern is defined to match all n+1 boundaries of an n-character
    text; it requires zero character comparisons.
    """
    if pattern == "":
        return list(range(len(text) + 1)), 0
    if len(pattern) > len(text):
        return [], 0

    matches: list[int] = []
    comparisons = 0
    for start in range(len(text) - len(pattern) + 1):
        offset = 0
        while offset < len(pattern):
            comparisons += 1
            if text[start + offset] != pattern[offset]:
                break
            offset += 1
        if offset == len(pattern):
            matches.append(start)
    return matches, comparisons


def main() -> None:
    cases = (
        ("easy", "dispatch priority", "patch"),
        ("repetitive", "A" * 12, "A" * 5 + "B"),
        ("overlapping", "ABABAABA", "ABA"),
    )
    for name, text, pattern in cases:
        matches, comparisons = brute_force_match(text, pattern)
        print(f"case={name} text_length={len(text)} pattern={pattern!r} matches_zero_based={matches} character_comparisons={comparisons}")


if __name__ == "__main__":
    main()