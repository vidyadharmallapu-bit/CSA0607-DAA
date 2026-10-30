"""Print and save original/corrected outputs plus insertion and alignment traces."""

from __future__ import annotations

from pathlib import Path

from CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code import corrected_module as corrected
from CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code import original_faulty_module as original
from CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code import optimized_module as optimized

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ALERTS = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
BLOCKLIST = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
QUERIES = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
LOG = "FAILFAIXFAIL"
PATTERN = "FAIL"
EVENTS = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]


def sort_trace() -> str:
    lines = ["STABLE INSERTION SORT TRACE (descending severity)"]
    alerts = ALERTS.copy()
    for index in range(1, len(alerts)):
        key = alerts[index]
        cursor = index - 1
        compared: list[str] = []
        shifts: list[str] = []
        while cursor >= 0:
            compared.append(f"{alerts[cursor]} vs key {key}")
            if alerts[cursor][1] >= key[1]:
                break
            shifts.append(f"move {alerts[cursor]} from {cursor} to {cursor + 1}")
            alerts[cursor + 1] = alerts[cursor]
            cursor -= 1
        insertion_position = cursor + 1
        alerts[insertion_position] = key
        lines.append(f"iteration={index} key={key}")
        lines.append(f"  comparisons={compared or ['none']}")
        lines.append(f"  shifts={shifts or ['none']}")
        lines.append(f"  insertion_position={insertion_position}; array={alerts}")
    return "\n".join(lines)


def matching_trace() -> str:
    lines = [f"BRUTE-FORCE ALIGNMENT TRACE text={LOG!r} pattern={PATTERN!r}"]
    for start in range(len(LOG) - len(PATTERN) + 1):
        compared: list[str] = []
        mismatch: int | None = None
        for offset, expected in enumerate(PATTERN):
            actual = LOG[start + offset]
            compared.append(f"text[{start + offset}]={actual!r} vs pattern[{offset}]={expected!r}")
            if actual != expected:
                mismatch = offset
                break
        matched = mismatch is None
        lines.append(f"start={start} comparisons={compared} mismatch_offset={mismatch} match={matched}")
    return "\n".join(lines)


def original_outputs() -> str:
    lines = ["ORIGINAL SUPPLIED PROGRAM OUTPUTS (logic unchanged)"]
    alerts = ALERTS.copy()
    lines.append(f"sort_alerts -> {original.sort_alerts(alerts)}")
    lines.append(f"is_blocked -> {[(query, original.is_blocked(BLOCKLIST, query)) for query in QUERIES]}")
    lines.append(f"find_signature({LOG!r}, {PATTERN!r}) -> {original.find_signature(LOG, PATTERN)}")
    pair, distance = original.closest_logins(EVENTS)
    lines.append(f"closest_logins -> pair={pair}, distance_km={distance:.12f}")
    try:
        original.find_signature("abc", "")
    except Exception as error:  # Record the observed original exception as evidence.
        lines.append(f"find_signature('abc', '') -> {type(error).__name__}: {error}")
    return "\n".join(lines)


def corrected_outputs(sort_details: str, match_details: str) -> str:
    alerts = ALERTS.copy()
    pair, distance = corrected.closest_logins(EVENTS)
    lines = [
        "CORRECTED PROGRAM OUTPUTS",
        f"sort_alerts -> {corrected.sort_alerts(alerts)}",
        f"is_blocked -> {[(query, corrected.is_blocked(BLOCKLIST, query)) for query in QUERIES]}",
        f"find_signature({LOG!r}, {PATTERN!r}) -> {corrected.find_signature(LOG, PATTERN)}",
        f"closest_logins -> pair={pair}, distance_km={distance:.12f}",
        "",
        sort_details,
        "",
        match_details,
    ]
    return "\n".join(lines)


def optimized_outputs() -> str:
    alerts = ALERTS.copy()
    sort_counts = optimized.insertion_sort_alerts_instrumented(alerts)
    block_index = optimized.BlocklistIndex(BLOCKLIST)
    blocked, search_counts = block_index.query_many(QUERIES)
    matching = optimized.find_signature_instrumented(LOG, PATTERN)
    brute = optimized.closest_logins_brute_force_instrumented(EVENTS)
    fast = optimized.closest_logins_instrumented(EVENTS)
    return "\n".join((
        "OPTIMIZED MODULE DEMONSTRATION",
        f"stable insertion sort -> {alerts}; counts={sort_counts}",
        f"indexed blocklist queries -> {blocked}; counts={search_counts}",
        f"counted brute-force signatures -> {matching.positions}; comparisons={matching.character_comparisons}",
        f"closest pair brute -> {brute.pair}, {brute.distance:.12f} km, distances={brute.distance_calculations}",
        f"closest pair divide-and-conquer -> {fast.pair}, {fast.distance:.12f} km, distances={fast.distance_calculations}, preprocessing={fast.preprocessing_operations}",
    ))


def main() -> None:
    original_text = original_outputs()
    sort_details = sort_trace()
    match_details = matching_trace()
    corrected_text = corrected_outputs(sort_details, match_details)
    optimized_text = optimized_outputs()
    original_folder = PROJECT_ROOT / "Output_Screenshots" / "original_outputs"
    corrected_folder = PROJECT_ROOT / "Output_Screenshots" / "corrected_outputs"
    original_folder.mkdir(parents=True, exist_ok=True)
    corrected_folder.mkdir(parents=True, exist_ok=True)
    optimized_folder = PROJECT_ROOT / "Output_Screenshots" / "optimized_outputs"
    optimized_folder.mkdir(parents=True, exist_ok=True)
    (original_folder / "original_run.txt").write_text(original_text + "\n", encoding="utf-8")
    (corrected_folder / "corrected_outputs_and_traces.txt").write_text(corrected_text + "\n", encoding="utf-8")
    (optimized_folder / "optimized_outputs.txt").write_text(optimized_text + "\n", encoding="utf-8")
    print(original_text)
    print("\n" + corrected_text)
    print("\n" + optimized_text)


if __name__ == "__main__":
    main()
