"""Run reproducible CO2 experiments, save measured CSVs, plots, and output logs."""

from __future__ import annotations

import csv
import platform
import random
import sys
from pathlib import Path
from time import perf_counter
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from CO2_Assignment.Q1_Sorting_Algorithms.Implementation_Code.sorting_algorithms import SORTS
from CO2_Assignment.Q2_Sequential_Search.Implementation_Code.sequential_search import make_records, sequential_search
from CO2_Assignment.Q3_Brute_Force_String_Matching.Implementation_Code.brute_force_string_matching import brute_force_match
from CO2_Assignment.Q4_Brute_Force_Closest_Pair.Implementation_Code.brute_force_closest_pair import closest_pair
from CO2_Assignment.Q5_Brute_Force_Convex_Hull.Implementation_Code.brute_force_convex_hull import convex_hull
from CO2_Assignment.Q6_Exhaustive_Search.Implementation_Code.exhaustive_knapsack import Package, exhaustive_knapsack
from CO2_Assignment.Q7_Day4_Design_Challenge.Implementation_Code.design_challenge import branch_and_bound_knapsack

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "Experimental_Data"
GRAPHS = ROOT / "Graphs"
ENVIRONMENT = f"Python {platform.python_version()}; {platform.platform()}"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write an empty experiment file: {path}")
    for row in rows:
        row["environment"] = ENVIRONMENT
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save_log(question: str, heading: str, lines: list[str]) -> None:
    folder = ROOT / question / "Output_Screenshots"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "execution_output.txt"
    path.write_text("\n".join([heading, f"Environment: {ENVIRONMENT}", *lines, ""]), encoding="utf-8")


def run_q1() -> list[dict[str, Any]]:
    datasets = {
        "reverse_sorted": (list(range(40, 0, -1)), "fixed descending integers 40..1"),
        "nearly_sorted": (list(range(40))[:], "ascending 0..39 with the final 6 values reversed"),
        "empty": ([], "empty edge-case list"),
    }
    datasets["nearly_sorted"][0][-6:] = reversed(datasets["nearly_sorted"][0][-6:])
    rows: list[dict[str, Any]] = []
    log = ["Prediction: insertion sort should benefit most from nearly sorted input; selection sort comparisons stay fixed for a given n; early-exit bubble sort should stop quickly on ordered input."]
    for dataset_name, (source, description) in datasets.items():
        for algorithm_name, algorithm in SORTS.items():
            values = source.copy()
            start = perf_counter()
            stats = algorithm(values)
            elapsed = perf_counter() - start
            correct = values == sorted(source)
            assert correct
            row = {
                "dataset": dataset_name,
                "description": description,
                "n": len(source),
                "algorithm": algorithm_name,
                "comparisons": stats.comparisons,
                "movements": stats.movements,
                "swaps": stats.swaps,
                "elapsed_seconds": f"{elapsed:.9f}",
                "correct": correct,
            }
            rows.append(row)
            log.append(f"{dataset_name:16s} {algorithm_name:18s} n={len(source):2d} comparisons={stats.comparisons:4d} movements={stats.movements:4d} swaps={stats.swaps:3d} seconds={elapsed:.9f} correct={correct}")
    write_csv(DATA / "q1_sorting_results.csv", rows)
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for axis, metric, title in zip(axes, ("comparisons", "movements"), ("Key comparisons", "Element movements")):
        labels = [f"{row['dataset']}\n{row['algorithm']}" for row in rows]
        axis.bar(range(len(rows)), [int(row[metric]) for row in rows], color=["#276FBF", "#F4A261", "#2A9D8F"] * 3)
        axis.set_xticks(range(len(rows)), labels, rotation=65, ha="right", fontsize=7)
        axis.set_title(title)
        axis.set_ylabel("count")
        axis.grid(axis="y", alpha=0.25)
    figure.suptitle("Q1: Sorting work by input condition")
    figure.tight_layout()
    figure.savefig(GRAPHS / "q1_sorting_operations.png", dpi=160)
    plt.close(figure)
    save_log("Q1_Sorting_Algorithms", "Q1 SORTING EXPERIMENT", log)
    return rows


def run_q2() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    log = ["Prediction: a hit at zero-based position p takes p+1 comparisons; a miss takes n comparisons."]
    for size in (10, 1000):
        records = make_records(size)
        for label, index, target in (
            ("first", 0, "T00000"),
            ("middle", size // 2, f"T{size // 2:05d}"),
            ("final", size - 1, f"T{size - 1:05d}"),
            ("miss", None, "NOT-ISSUED"),
        ):
            found_index, comparisons = sequential_search(records, target)
            correct = found_index == index and comparisons == (index + 1 if index is not None else size)
            assert correct
            row = {"n": size, "case": label, "target_tool_id": target, "target_position_zero_based": index if index is not None else "not_found", "found": found_index is not None, "comparisons": comparisons, "dataset": f"deterministic generated IDs T00000..T{size - 1:05d}", "correct": correct}
            rows.append(row)
            log.append(f"n={size:4d} case={label:6s} position={str(index):>4s} found={found_index is not None!s:5s} comparisons={comparisons:4d} correct={correct}")
    write_csv(DATA / "q2_search_results.csv", rows)
    save_log("Q2_Sequential_Search", "Q2 SEQUENTIAL SEARCH EXPERIMENT", log)
    return rows


def run_q3() -> list[dict[str, Any]]:
    cases = (
        ("easy_early", "dispatch priority", "patch", "Short pattern occurs near the beginning."),
        ("repetitive_worst_style", "A" * 80, "A" * 20 + "B", "Repeated A prefixes force a long failed comparison at many shifts."),
        ("overlapping_multiple", "ABABAABA", "ABA", "Multiple overlapping occurrences are present."),
    )
    rows = []
    log = ["Prediction: repetitive near-matches should require far more comparisons than a similarly sized easy match; overlapping hits are retained."]
    for name, text, pattern, description in cases:
        matches, comparisons = brute_force_match(text, pattern)
        expected = []
        if pattern:
            start = 0
            while True:
                start = text.find(pattern, start)
                if start < 0:
                    break
                expected.append(start)
                start += 1
        else:
            expected = list(range(len(text) + 1))
        correct = matches == expected
        assert correct
        rows.append({"case": name, "description": description, "text_length": len(text), "pattern_length": len(pattern), "matches_zero_based": ";".join(map(str, matches)), "character_comparisons": comparisons, "prediction": "repetitive near-match has high work; overlaps are reported" if "repetitive" in name or "overlapping" in name else "early match uses few comparisons", "correct": correct})
        log.append(f"case={name} n={len(text)} m={len(pattern)} matches={matches} comparisons={comparisons} independently_validated={correct}")
    write_csv(DATA / "q3_string_matching_results.csv", rows)
    save_log("Q3_Brute_Force_String_Matching", "Q3 BRUTE-FORCE STRING MATCHING EXPERIMENT", log)
    return rows


def run_q4() -> list[dict[str, Any]]:
    rows = []
    log = ["Acceptance criterion set before measurement: one closest-pair run should finish within 1.0 second on this environment; this is a local threshold, not a hardware-independent limit."]
    for size in (10, 100, 500, 1500, 3000, 5000):
        seed = 4200 + size
        rng = random.Random(seed)
        points = [(rng.uniform(-1000, 1000), rng.uniform(-1000, 1000)) for _ in range(size)]
        start = perf_counter()
        result = closest_pair(points)
        elapsed = perf_counter() - start
        expected_pairs = size * (size - 1) // 2
        independent_distance = min(((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2) ** 0.5 for index, first in enumerate(points) for second in points[index + 1:])
        correct = result.pairs_examined == expected_pairs and result.distance_calculations == expected_pairs and abs(result.distance - independent_distance) < 1e-12
        assert correct
        rows.append({"n_points": size, "seed": seed, "expected_pair_count": expected_pairs, "actual_pair_count": result.pairs_examined, "distance_calculations": result.distance_calculations, "elapsed_seconds": f"{elapsed:.9f}", "acceptance_seconds": 1.0, "within_acceptance": elapsed <= 1.0, "closest_distance": f"{result.distance:.9f}", "correct": correct})
        log.append(f"n={size:3d} expected_pairs={expected_pairs:7d} actual_pairs={result.pairs_examined:7d} distance_calcs={result.distance_calculations:7d} seconds={elapsed:.6f} accepted={elapsed <= 1.0} correct={correct}")
    write_csv(DATA / "q4_closest_pair_results.csv", rows)
    figure, axis = plt.subplots(figsize=(7, 4.5))
    sizes = [int(row["n_points"]) for row in rows]
    axis.plot(sizes, [int(row["expected_pair_count"]) for row in rows], marker="o", label="Theoretical n(n-1)/2")
    axis.scatter(sizes, [int(row["actual_pair_count"]) for row in rows], marker="x", s=70, label="Measured pair count")
    axis.set(title="Q4: Closest-pair comparisons", xlabel="Number of points", ylabel="Pairs examined")
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(GRAPHS / "q4_closest_pair_counts.png", dpi=160)
    plt.close(figure)
    save_log("Q4_Brute_Force_Closest_Pair", "Q4 BRUTE-FORCE CLOSEST-PAIR EXPERIMENT", log)
    return rows


def point_inside_convex_polygon(point: tuple[float, float], polygon: list[tuple[float, float]]) -> bool:
    from CO2_Assignment.Q5_Brute_Force_Convex_Hull.Implementation_Code.brute_force_convex_hull import orientation

    signs = [orientation(polygon[index], polygon[(index + 1) % len(polygon)], point) for index in range(len(polygon))]
    return all(value >= 0 for value in signs) or all(value <= 0 for value in signs)


def run_q5() -> list[dict[str, Any]]:
    configurations = {
        "boundary_and_interior": ([(0, 0), (4, 0), (4, 3), (0, 3), (2, 1), (1, 2), (3, 2)], {(0, 0), (4, 0), (4, 3), (0, 3)}),
        "collinear_duplicates_symmetric": ([(0, 0), (2, 0), (4, 0), (4, 2), (4, 4), (2, 4), (0, 4), (0, 2), (2, 2), (0, 0), (1, 1)], {(0, 0), (4, 0), (4, 4), (0, 4)}),
    }
    rows = []
    log = ["Prediction: supporting candidate lines identify the outer boundary; intermediate collinear points, duplicates, and interior points are excluded from polygon corners."]
    for name, (points, expected) in configurations.items():
        result = convex_hull(points)
        correct = set(result.vertices) == expected and len(result.vertices) == len(expected) and all(point_inside_convex_polygon(point, result.vertices) for point in set(points))
        assert correct, (name, result.vertices)
        rows.append({"configuration": name, "input_count": len(points), "unique_points": len(set(points)), "hull_vertices": ";".join(f"{x}:{y}" for x, y in result.vertices), "hull_vertex_count": len(result.vertices), "candidate_pairs": result.candidate_pairs, "orientation_tests": result.orientation_tests, "correct": correct})
        log.append(f"case={name} input={len(points)} unique={len(set(points))} hull={result.vertices} pairs={result.candidate_pairs} orientation_tests={result.orientation_tests} correct={correct}")
        figure, axis = plt.subplots(figsize=(6, 5))
        unique_points = list(dict.fromkeys(points))
        axis.scatter([p[0] for p in unique_points], [p[1] for p in unique_points], color="#276FBF", label="Input points")
        for index, point in enumerate(unique_points):
            axis.annotate(str(point), point, xytext=(4, 4), textcoords="offset points", fontsize=8)
        closed = result.vertices + result.vertices[:1] if len(result.vertices) > 2 else result.vertices
        if closed:
            axis.plot([p[0] for p in closed], [p[1] for p in closed], color="#E76F51", marker="o", label="Hull boundary")
        axis.set(title=f"Q5: {name.replace('_', ' ')}", xlabel="x", ylabel="y", aspect="equal")
        axis.grid(alpha=0.2)
        axis.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8)
        figure.tight_layout(rect=(0, 0, 0.78, 1))
        figure.savefig(GRAPHS / f"q5_{name}.png", dpi=160)
        plt.close(figure)
    write_csv(DATA / "q5_convex_hull_results.csv", rows)
    save_log("Q5_Brute_Force_Convex_Hull", "Q5 BRUTE-FORCE CONVEX HULL EXPERIMENT", log)
    return rows


def make_q6_packages(size: int, seed: int) -> list[Package]:
    rng = random.Random(seed)
    return [Package(f"PKG{i:02d}", rng.randint(1, 40), rng.randint(1, 100)) for i in range(size)]


def run_q6() -> list[dict[str, Any]]:
    rows = []
    log = ["Prediction: each added package doubles the examined subset count. The local response budget is 2.0 seconds for an exhaustive solve."]
    for size in (10, 15, 18, 19, 20):
        seed = 6010 + size
        packages = make_q6_packages(size, seed)
        capacity = sum(item.weight for item in packages) * 3 // 10
        start = perf_counter()
        result = exhaustive_knapsack(packages, capacity)
        elapsed = perf_counter() - start
        valid_ids = {item.package_id for item in packages}
        correct = result.subsets_examined == 2 ** size and result.total_weight <= capacity and set(result.package_ids) <= valid_ids
        assert correct
        rows.append({"n_packages": size, "seed": seed, "capacity": capacity, "subsets_expected": 2 ** size, "subsets_examined": result.subsets_examined, "feasible_subsets": result.feasible_subsets, "best_value": result.total_value, "best_weight": result.total_weight, "elapsed_seconds": f"{elapsed:.9f}", "response_budget_seconds": 2.0, "within_budget": elapsed <= 2.0, "correct": correct})
        log.append(f"n={size:2d} capacity={capacity:4d} expected_subsets={2 ** size:8d} actual={result.subsets_examined:8d} feasible={result.feasible_subsets:8d} best={result.total_value:4d} weight={result.total_weight:4d} seconds={elapsed:.6f} within_budget={elapsed <= 2.0} correct={correct}")
    write_csv(DATA / "q6_exhaustive_search_results.csv", rows)
    figure, axis = plt.subplots(figsize=(7, 4.5))
    sizes = [int(row["n_packages"]) for row in rows]
    axis.plot(sizes, [2 ** size for size in sizes], marker="o", label="Theoretical 2^n")
    axis.scatter(sizes, [int(row["subsets_examined"]) for row in rows], marker="x", s=70, label="Measured subsets")
    axis.set_yscale("log", base=2)
    axis.set(title="Q6: Exhaustive subset growth", xlabel="Number of packages", ylabel="Subsets (log2 scale)")
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(GRAPHS / "q6_subset_growth.png", dpi=160)
    plt.close(figure)
    save_log("Q6_Exhaustive_Search", "Q6 EXHAUSTIVE KNAPSACK EXPERIMENT", log)
    return rows


def q7_datasets() -> dict[str, tuple[list[Package], int, int]]:
    effective_rng = random.Random(77020)
    effective = [Package(f"E{i:02d}", effective_rng.randint(2, 45), effective_rng.randint(2, 140)) for i in range(20)]
    weak = [Package(f"W{i:02d}", 2, 2) for i in range(17)]
    return {
        "diverse_ratios_effective_pruning": (effective, sum(item.weight for item in effective) // 3, 77020),
        "equal_ratio_weak_pruning": (weak, 16, 77117),
    }


def run_q7() -> list[dict[str, Any]]:
    rows = []
    log = ["Pre-implementation prediction: diverse value/weight ratios will let the fractional bound prune large subtrees; equal-ratio packages will weaken pruning, so visited nodes may approach exhaustive scale."]
    for name, (packages, capacity, seed) in q7_datasets().items():
        start = perf_counter()
        original = exhaustive_knapsack(packages, capacity)
        original_seconds = perf_counter() - start
        redesigned = branch_and_bound_knapsack(packages, capacity)
        redesigned_total = redesigned.preprocessing_seconds + redesigned.search_seconds
        valid_ids = {item.package_id for item in packages}
        correct = (original.total_value, original.total_weight, original.package_ids) == (redesigned.total_value, redesigned.total_weight, redesigned.package_ids) and original.total_weight <= capacity and redesigned.total_weight <= capacity and set(original.package_ids) <= valid_ids and set(redesigned.package_ids) <= valid_ids
        assert correct, (name, original, redesigned)
        rows.append({"dataset": name, "seed": seed, "n_packages": len(packages), "capacity": capacity, "original_candidate_subsets": original.subsets_examined, "original_feasible_subsets": original.feasible_subsets, "original_best_value": original.total_value, "original_best_weight": original.total_weight, "original_elapsed_seconds": f"{original_seconds:.9f}", "bnb_visited_nodes": redesigned.visited_nodes, "bnb_expanded_nodes": redesigned.expanded_nodes, "bnb_pruned_nodes": redesigned.pruned_nodes, "bnb_complete_subsets_evaluated": redesigned.complete_subsets_evaluated, "bnb_best_value": redesigned.total_value, "bnb_best_weight": redesigned.total_weight, "bnb_preprocessing_seconds": f"{redesigned.preprocessing_seconds:.9f}", "bnb_search_seconds": f"{redesigned.search_seconds:.9f}", "bnb_total_seconds": f"{redesigned_total:.9f}", "complete_candidate_reduction_fraction": f"{1 - redesigned.complete_subsets_evaluated / original.subsets_examined:.9f}", "correct": correct})
        log.append(f"case={name} n={len(packages)} subsets={original.subsets_examined} BnB_nodes={redesigned.visited_nodes} complete_leaves={redesigned.complete_subsets_evaluated} expanded={redesigned.expanded_nodes} pruned={redesigned.pruned_nodes} exhaustive_s={original_seconds:.6f} BnB_pre_s={redesigned.preprocessing_seconds:.6f} BnB_search_s={redesigned.search_seconds:.6f} values_match={correct}")
    write_csv(DATA / "q7_redesign_comparison.csv", rows)
    figure, axis = plt.subplots(figsize=(9, 5))
    x_positions = list(range(len(rows)))
    width = 0.36
    original_counts = [int(row["original_candidate_subsets"]) for row in rows]
    visited_counts = [int(row["bnb_visited_nodes"]) for row in rows]
    axis.bar([x - width / 2 for x in x_positions], original_counts, width, label="Exhaustive subsets", color="#276FBF")
    axis.bar([x + width / 2 for x in x_positions], visited_counts, width, label="Branch-and-bound visited nodes", color="#E76F51")
    axis.set_yscale("log", base=2)
    axis.set_xticks(x_positions, [row["dataset"].replace("_", "\n") for row in rows], fontsize=8)
    axis.set(title="Q7: Search effort on identical instances", ylabel="Candidates / visited nodes (log2 scale)")
    axis.grid(axis="y", alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(GRAPHS / "q7_search_effort.png", dpi=160)
    plt.close(figure)
    save_log("Q7_Day4_Design_Challenge", "Q7 EXHAUSTIVE VS BRANCH-AND-BOUND", log)
    return rows


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    GRAPHS.mkdir(parents=True, exist_ok=True)
    print(f"CO2 experiment suite | {ENVIRONMENT}")
    for question, runner in (("Q1", run_q1), ("Q2", run_q2), ("Q3", run_q3), ("Q4", run_q4), ("Q5", run_q5), ("Q6", run_q6), ("Q7", run_q7)):
        rows = runner()
        print(f"{question}: wrote {len(rows)} verified records")
    print(f"CSV data: {DATA}")
    print(f"Graphs: {GRAPHS}")
    print("Per-question execution logs are in each Output_Screenshots folder; they are logs, not screenshots.")


if __name__ == "__main__":
    main()
