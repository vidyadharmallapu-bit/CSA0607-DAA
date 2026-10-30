"""Generate reproducible measured CSVs, graphs, and benchmark output logs."""

from __future__ import annotations

import csv
import math
import platform
import random
import string
import time
from pathlib import Path
from typing import Any, Callable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code import corrected_module as corrected
from CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code import optimized_module as optimized

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUPPORT = PROJECT_ROOT / "Supporting_Files"
GRAPHS = SUPPORT / "graphs"
OUTPUT = PROJECT_ROOT / "Output_Screenshots" / "benchmark_outputs"
ENVIRONMENT = f"Python {platform.python_version()}; {platform.platform()}"


def write_csv(filename: str, rows: list[dict[str, Any]]) -> Path:
    if not rows:
        raise ValueError(f"cannot save an empty benchmark: {filename}")
    for row in rows:
        row["environment"] = ENVIRONMENT
    path = SUPPORT / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def stable(source: list[tuple[str, int]], result: list[tuple[str, int]]) -> bool:
    return result == sorted(source, key=lambda alert: -alert[1])


def sorting_benchmarks(lines: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sizes = (100, 1000, 5000)
    seed = 8821
    rng = random.Random(seed)
    for size in sizes:
        random_alerts = [(f"R{index:05d}", rng.randrange(1, 101)) for index in range(size)]
        nearly = sorted(random_alerts, key=lambda alert: -alert[1])
        for index in range(0, max(0, size - 1), max(1, size // 100)):
            if index + 1 < size:
                nearly[index], nearly[index + 1] = nearly[index + 1], nearly[index]
        datasets = {
            "nearly_sorted": nearly,
            "random": random_alerts,
            "reverse_sorted": sorted(random_alerts, key=lambda alert: alert[1]),
        }
        for dataset_name, source in datasets.items():
            for algorithm_name, algorithm in (("insertion", optimized.insertion_sort_alerts_instrumented), ("stable_merge", optimized.stable_merge_sort_alerts_instrumented)):
                values = source.copy()
                start = time.perf_counter()
                counts = algorithm(values)
                elapsed = time.perf_counter() - start
                correct = stable(source, values)
                rows.append({"algorithm": algorithm_name, "dataset_type": dataset_name, "input_size": size, "seed": seed, "comparisons": counts.comparisons, "element_movements": counts.movements, "elapsed_seconds": f"{elapsed:.9f}", "correct": correct, "stability_preserved": correct})
                assert correct
                lines.append(f"sort {dataset_name:14s} n={size:5d} {algorithm_name:11s} comparisons={counts.comparisons:10d} movements={counts.movements:10d} seconds={elapsed:.6f} stable={correct}")
    return rows


def search_benchmarks(lines: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for size in (100, 1000, 10000):
        blocklist = [f"10.{index // 65536}.{(index // 256) % 256}.{index % 256}" for index in range(size)]
        rng = random.Random(8822 + size)
        queries = [blocklist[rng.randrange(size)] if index % 2 == 0 else f"192.0.2.{index % 256}" for index in range(500)]
        expected = [corrected.is_blocked(blocklist, query) for query in queries]
        comparison_count = 0
        start = time.perf_counter()
        sequential_results: list[bool] = []
        for query in queries:
            result = False
            for entry in blocklist:
                comparison_count += 1
                if entry == query:
                    result = True
                    break
            sequential_results.append(result)
        sequential_seconds = time.perf_counter() - start

        build_start = time.perf_counter()
        index = optimized.BlocklistIndex(blocklist)
        build_seconds = time.perf_counter() - build_start
        query_start = time.perf_counter()
        indexed_results, counts = index.query_many(queries)
        indexed_query_seconds = time.perf_counter() - query_start
        correct = sequential_results == expected == indexed_results
        assert correct
        rows.append({"blocklist_entries": size, "query_count": len(queries), "hit_ratio": "0.5", "index_construction_seconds": f"{build_seconds:.9f}", "sequential_comparisons": comparison_count, "sequential_total_seconds": f"{sequential_seconds:.9f}", "indexed_build_operations": counts.index_build_operations, "indexed_lookup_count": counts.lookups, "indexed_query_seconds": f"{indexed_query_seconds:.9f}", "indexed_total_seconds": f"{build_seconds + indexed_query_seconds:.9f}", "correct": correct, "seed": 8822 + size})
        lines.append(f"search n={size:5d} queries=500 comparisons={comparison_count:9d} sequential={sequential_seconds:.6f}s index_build={build_seconds:.6f}s set_queries={indexed_query_seconds:.6f}s correct={correct}")
    return rows


def string_benchmarks(lines: list[str]) -> list[dict[str, Any]]:
    cases = (
        ("early_match", "SIGNATURE:" + "X" * 3990, "SIGNATURE"),
        ("repetitive_near_match", "A" * 6000, "A" * 99 + "B"),
        ("missing_pattern", "ABCDEFGH" * 500, "XYZ"),
        ("overlapping_matches", "AB" * 2000, "ABA"),
    )
    rows = []
    for case_name, text, pattern in cases:
        start = time.perf_counter()
        result = optimized.find_signature_instrumented(text, pattern)
        elapsed = time.perf_counter() - start
        expected = []
        offset = 0
        while pattern:
            offset = text.find(pattern, offset)
            if offset < 0:
                break
            expected.append(offset)
            offset += 1
        if pattern == "":
            expected = list(range(len(text) + 1))
        correct = result.positions == expected
        assert correct
        rows.append({"case": case_name, "text_length": len(text), "pattern_length": len(pattern), "character_comparisons": result.character_comparisons, "match_count": len(result.positions), "match_positions_sample": ";".join(map(str, result.positions[:10])), "elapsed_seconds": f"{elapsed:.9f}", "correct": correct})
        lines.append(f"string {case_name:22s} n={len(text):5d} m={len(pattern):3d} comparisons={result.character_comparisons:8d} matches={len(result.positions):5d} seconds={elapsed:.6f} correct={correct}")
    return rows


def make_points(size: int, seed: int) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    return [(rng.uniform(-10000.0, 10000.0), rng.uniform(-10000.0, 10000.0)) for _ in range(size)]


def closest_pair_benchmarks(lines: list[str]) -> list[dict[str, Any]]:
    rows = []
    for size in (1000, 2000, 4000, 8000):
        seed = 8830 + size
        events = make_points(size, seed)
        theoretical_pairs = size * (size - 1) // 2
        start = time.perf_counter()
        brute = optimized.closest_logins_brute_force_instrumented(events)
        brute_seconds = time.perf_counter() - start
        start = time.perf_counter()
        fast = optimized.closest_logins_instrumented(events)
        optimized_seconds = time.perf_counter() - start
        correct = (brute.pair, brute.distance) == (fast.pair, fast.distance)
        assert correct
        assert brute.candidate_pairs == theoretical_pairs
        rows.append({"event_count": size, "seed": seed, "theoretical_unique_pairs": theoretical_pairs, "brute_candidate_pairs": brute.candidate_pairs, "brute_distance_calculations": brute.distance_calculations, "brute_preprocessing_operations": brute.preprocessing_operations, "brute_elapsed_seconds": f"{brute_seconds:.9f}", "optimized_candidate_pairs": fast.candidate_pairs, "optimized_distance_calculations": fast.distance_calculations, "optimized_preprocessing_operations": fast.preprocessing_operations, "optimized_elapsed_seconds": f"{optimized_seconds:.9f}", "minimum_distance_km": f"{fast.distance:.12f}", "distance_calculation_reduction_fraction": f"{1 - fast.distance_calculations / brute.distance_calculations:.9f}", "correct": correct})
        lines.append(f"closest n={size:5d} theoretical={theoretical_pairs:11d} brute_dists={brute.distance_calculations:11d} optimized_dists={fast.distance_calculations:8d} preprocessing_ops={fast.preprocessing_operations:9d} brute={brute_seconds:.4f}s optimized={optimized_seconds:.4f}s min={fast.distance:.8f} agreement={correct}")
    return rows


def make_graphs(paths: dict[str, Path]) -> None:
    GRAPHS.mkdir(parents=True, exist_ok=True)

    sorting = read_csv(paths["sorting"])
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for algorithm, marker in (("insertion", "o"), ("stable_merge", "s")):
        for dataset in ("nearly_sorted", "random", "reverse_sorted"):
            group = [row for row in sorting if row["algorithm"] == algorithm and row["dataset_type"] == dataset]
            axes[0].plot([int(row["input_size"]) for row in group], [int(row["comparisons"]) for row in group], marker=marker, label=f"{algorithm}: {dataset}")
            axes[1].plot([int(row["input_size"]) for row in group], [float(row["elapsed_seconds"]) for row in group], marker=marker, label=f"{algorithm}: {dataset}")
    axes[0].set(title="Alert sorting comparisons", xlabel="Alerts", ylabel="Key comparisons")
    axes[1].set(title="Alert sorting elapsed time", xlabel="Alerts", ylabel="Seconds")
    for axis in axes:
        axis.grid(alpha=0.25)
        axis.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(GRAPHS / "sorting_benchmarks.png", dpi=160)
    plt.close(fig)

    search = read_csv(paths["search"])
    fig, axis = plt.subplots(figsize=(7, 4.5))
    axis.plot([int(row["blocklist_entries"]) for row in search], [float(row["sequential_total_seconds"]) for row in search], marker="o", label="Sequential queries")
    axis.plot([int(row["blocklist_entries"]) for row in search], [float(row["indexed_total_seconds"]) for row in search], marker="s", label="Set build + queries")
    axis.set(title="Repeated blocklist lookup workload", xlabel="Blocklist entries", ylabel="Seconds", xscale="log")
    axis.grid(alpha=0.25)
    axis.legend()
    fig.tight_layout()
    fig.savefig(GRAPHS / "blocklist_benchmarks.png", dpi=160)
    plt.close(fig)

    strings = read_csv(paths["strings"])
    fig, axis = plt.subplots(figsize=(8, 4.5))
    axis.bar([row["case"] for row in strings], [int(row["character_comparisons"]) for row in strings], color="#277DA1")
    axis.set(title="Brute-force signature comparisons", ylabel="Character comparisons")
    axis.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(GRAPHS / "string_benchmarks.png", dpi=160)
    plt.close(fig)

    closest = read_csv(paths["closest"])
    fig, axis = plt.subplots(figsize=(8, 4.5))
    sizes = [int(row["event_count"]) for row in closest]
    axis.plot(sizes, [int(row["brute_distance_calculations"]) for row in closest], marker="o", label="Unique-pair brute force")
    axis.plot(sizes, [int(row["optimized_distance_calculations"]) for row in closest], marker="s", label="Divide and conquer")
    axis.plot(sizes, [int(row["theoretical_unique_pairs"]) for row in closest], linestyle="--", label="n(n-1)/2")
    axis.set(title="Exact closest-pair distance calculations", xlabel="Login events", ylabel="Distance calculations", yscale="log")
    axis.grid(alpha=0.25)
    axis.legend()
    fig.tight_layout()
    fig.savefig(GRAPHS / "closest_pair_benchmarks.png", dpi=160)
    plt.close(fig)


def main() -> None:
    SUPPORT.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    lines = ["SENTINELOPS OPTIMIZATION BENCHMARKS", f"Environment: {ENVIRONMENT}", "Operation counts and timings are recorded separately."]
    paths = {
        "sorting": write_csv("sorting_benchmarks.csv", sorting_benchmarks(lines)),
        "search": write_csv("search_benchmarks.csv", search_benchmarks(lines)),
        "strings": write_csv("string_matching_benchmarks.csv", string_benchmarks(lines)),
        "closest": write_csv("closest_pair_benchmarks.csv", closest_pair_benchmarks(lines)),
    }
    make_graphs(paths)
    log_path = OUTPUT / "benchmark_results.txt"
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nCSV and graph output: {SUPPORT}")
    print(f"Benchmark log: {log_path}")


if __name__ == "__main__":
    main()
