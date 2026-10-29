"""Sequential search over deterministic aircraft-tool issue records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence


@dataclass(frozen=True)
class ToolIssue:
    tool_id: str
    technician_id: str
    issue_time: str
    work_bay: str


def sequential_search(records: Sequence[ToolIssue], target_tool_id: str) -> tuple[int | None, int]:
    """Return the first matching index and key-comparison count."""
    comparisons = 0
    for index, record in enumerate(records):
        comparisons += 1
        if record.tool_id == target_tool_id:
            return index, comparisons
    return None, comparisons


def make_records(size: int) -> list[ToolIssue]:
    if size < 0:
        raise ValueError("size must be nonnegative")
    return [ToolIssue(f"T{index:05d}", f"TECH{index % 17:02d}", f"2026-10-29T{index % 24:02d}:00", f"BAY{index % 8:02d}") for index in range(size)]


def main() -> None:
    records = make_records(10)
    for target in ("T00000", "T00005", "T00009", "missing"):
        index, comparisons = sequential_search(records, target)
        print(f"n={len(records)} target={target} position={index} found={index is not None} comparisons={comparisons}")


if __name__ == "__main__":
    main()