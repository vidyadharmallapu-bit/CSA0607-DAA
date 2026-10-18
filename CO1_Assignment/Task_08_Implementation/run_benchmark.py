"""Reproducible timing experiment; writes CSV and an SVG graph."""

import csv
import math
import random
import statistics
import time
from pathlib import Path
from typing import Callable, Dict, List, Sequence

from search_algorithms import hash_search, linear_search, recursive_binary_search


SIZES = (1_000, 10_000, 100_000, 1_000_000)
QUERIES_PER_ROUND = 30
REPETITIONS = 5
CHALLENGE_SEARCHES_PER_HOUR = 50_000
OUTPUT_DIRECTORY = (
    Path(__file__).resolve().parents[1] / "Task_09_Performance_Analysis"
)


def make_registration_number(value: int) -> str:
    return "STU{:07d}".format(value)


def make_queries(size: int) -> List[str]:
    hits = [make_registration_number(size * part // 16) for part in range(1, 16)]
    misses = [make_registration_number(size + offset) for offset in range(15)]
    return [query for pair in zip(hits, misses) for query in pair]


def median_seconds_per_query(
    search: Callable[[Sequence[str], str], object],
    records: Sequence[str],
    queries: Sequence[str],
) -> float:
    samples = []
    for _ in range(REPETITIONS):
        start = time.perf_counter()
        for target in queries:
            search(records, target)
        elapsed = time.perf_counter() - start
        samples.append(elapsed / len(queries))
    return statistics.median(samples)


def median_mapping_seconds_per_query(index: Dict[str, str], queries: Sequence[str]) -> float:
    samples = []
    for _ in range(REPETITIONS):
        start = time.perf_counter()
        for target in queries:
            hash_search(index, target)
        elapsed = time.perf_counter() - start
        samples.append(elapsed / len(queries))
    return statistics.median(samples)


def create_svg(rows: Sequence[Dict[str, object]], destination: Path) -> None:
    width, height = 900, 560
    left, right, top, bottom = 105, 45, 65, 90
    plot_width = width - left - right
    plot_height = height - top - bottom
    x_min, x_max = 1_000, 1_000_000
    y_min, y_max = 1e-8, 1.0

    def x_position(value: float) -> float:
        fraction = (math.log10(value) - math.log10(x_min)) / (
            math.log10(x_max) - math.log10(x_min)
        )
        return left + fraction * plot_width

    def y_position(value: float) -> float:
        ratio = (math.log10(max(value, y_min)) - math.log10(y_min)) / (
            math.log10(y_max) - math.log10(y_min)
        )
        return top + (1 - ratio) * plot_height

    sizes = [int(row["input_size"]) for row in rows]
    series = [
        ("Linear scan", "C63D3D", "linear_search_seconds_per_query"),
        ("Recursive binary search", "3267A8", "binary_search_seconds_per_query"),
        ("Hash index lookup", "248447", "hash_search_seconds_per_query"),
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#222}.grid{stroke:#ddd;stroke-width:1}.axis{stroke:#333;stroke-width:1.5}</style>',
        f'<text x="{width/2}" y="30" text-anchor="middle" font-size="20">Measured search time by dataset size</text>',
    ]

    for exponent in range(-8, 1, 2):
        value = 10.0 ** exponent
        y = y_position(value)
        parts.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}"/>')
        parts.append(f'<text x="{left-12}" y="{y+5:.1f}" text-anchor="end" font-size="12">10^{exponent} s</text>')
    for size in sizes:
        x = x_position(size)
        parts.append(f'<line class="grid" x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}"/>')
        parts.append(f'<text x="{x:.1f}" y="{height-bottom+24}" text-anchor="middle" font-size="12">{size:,}</text>')
    parts.extend(
        [
            f'<line class="axis" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}"/>',
            f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}"/>',
            f'<text x="{width/2}" y="{height-24}" text-anchor="middle" font-size="14">Number of registration numbers (log scale)</text>',
            f'<text transform="translate(24 {height/2}) rotate(-90)" text-anchor="middle" font-size="14">Median seconds per request (log scale)</text>',
        ]
    )
    for label, color, field in series:
        points = [
            (x_position(float(row["input_size"])), y_position(float(row[field])))
            for row in rows
        ]
        point_string = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        parts.append(f'<polyline points="{point_string}" fill="none" stroke="#{color}" stroke-width="3"/>')
        for x, y in points:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#{color}"/>')
    for index, (label, color, _) in enumerate(series):
        y = 48 + index * 18
        x = width - right - 245
        parts.append(f'<line x1="{x}" y1="{y}" x2="{x+22}" y2="{y}" stroke="#{color}" stroke-width="3"/>')
        parts.append(f'<text x="{x+28}" y="{y+5}" font-size="12">{label}</text>')
    parts.append("</svg>")
    destination.write_text("\n".join(parts), encoding="utf-8")


def run() -> Path:
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIRECTORY / "performance.csv"
    rows = []

    for size in SIZES:
        generator = random.Random(20261016 + size)
        records = [make_registration_number(value) for value in range(size)]
        generator.shuffle(records)
        queries = make_queries(size)
        sorted_records = None
        hash_index = None

        start = time.perf_counter()
        sorted_records = sorted(records)
        binary_sort_seconds = time.perf_counter() - start

        start = time.perf_counter()
        hash_index = {record: record for record in records}
        hash_build_seconds = time.perf_counter() - start

        for target in queries:
            present = target in hash_index
            assert (linear_search(records, target) is not None) == present
            assert (recursive_binary_search(sorted_records, target) is not None) == present
            assert (hash_search(hash_index, target) is not None) == present

        linear_seconds = median_seconds_per_query(linear_search, records, queries)
        binary_seconds = median_seconds_per_query(
            recursive_binary_search, sorted_records, queries
        )
        hash_seconds = median_mapping_seconds_per_query(hash_index, queries)

        row = {
            "input_size": size,
            "queries_per_round": QUERIES_PER_ROUND,
            "repetitions": REPETITIONS,
            "linear_search_seconds_per_query": linear_seconds,
            "binary_sort_seconds": binary_sort_seconds,
            "binary_search_seconds_per_query": binary_seconds,
            "hash_build_seconds": hash_build_seconds,
            "hash_search_seconds_per_query": hash_seconds,
            "linear_50000_searches_seconds": linear_seconds * CHALLENGE_SEARCHES_PER_HOUR,
            "binary_build_plus_50000_searches_seconds": (
                binary_sort_seconds + binary_seconds * CHALLENGE_SEARCHES_PER_HOUR
            ),
            "hash_build_plus_50000_searches_seconds": (
                hash_build_seconds + hash_seconds * CHALLENGE_SEARCHES_PER_HOUR
            ),
        }
        rows.append(row)
        print(
            "n={:,}: linear={:.9f}s/query, binary={:.9f}s/query, "
            "hash={:.9f}s/query".format(size, linear_seconds, binary_seconds, hash_seconds)
        )
        del hash_index, sorted_records, records

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    create_svg(rows, OUTPUT_DIRECTORY / "search_time.svg")
    return csv_path


if __name__ == "__main__":
    print("Wrote measured results to {}".format(run()))
