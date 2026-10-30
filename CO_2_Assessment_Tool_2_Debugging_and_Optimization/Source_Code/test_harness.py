"""Standard-library regression tests for original, corrected, and optimized code."""

from __future__ import annotations

import csv
import io
import math
import sys
import unittest
from pathlib import Path

from CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code import corrected_module as corrected
from CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code import optimized_module as optimized
from CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code import original_faulty_module as original

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUPPLIED_ALERTS = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
SUPPLIED_BLOCKLIST = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
SUPPLIED_LOG = "FAILFAIXFAIL"
SUPPLIED_EVENTS = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]


class SentinelOpsTests(unittest.TestCase):
    def test_original_faulty_behaviour_is_preserved(self) -> None:
        alerts = SUPPLIED_ALERTS.copy()
        original.sort_alerts(alerts)
        self.assertNotEqual(alerts, [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)])
        self.assertEqual(original.is_blocked(SUPPLIED_BLOCKLIST, "10.0.0.9"), False)
        self.assertEqual(original.find_signature(SUPPLIED_LOG, "FAIL"), [0, 4])
        pair, distance = original.closest_logins(SUPPLIED_EVENTS)
        self.assertEqual(pair, (0, 2))
        self.assertAlmostEqual(distance, math.dist(SUPPLIED_EVENTS[0], SUPPLIED_EVENTS[2]))
        with self.assertRaises(UnboundLocalError):
            original.find_signature("abc", "")

    def test_sort_empty_single_sorted_reverse_and_stability(self) -> None:
        cases = [
            [],
            [("only", 4)],
            [("a", 9), ("b", 5), ("c", 1)],
            [("a", 1), ("b", 5), ("c", 9)],
            [("first-9", 9), ("middle-3", 3), ("second-9", 9), ("last-3", 3)],
        ]
        for source in cases:
            with self.subTest(source=source):
                values = source.copy()
                returned = corrected.sort_alerts(values)
                self.assertIs(returned, values)
                self.assertEqual(values, sorted(source, key=lambda alert: -alert[1]))
        supplied = SUPPLIED_ALERTS.copy()
        self.assertIs(corrected.sort_alerts(supplied), supplied)
        self.assertEqual(supplied, [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)])

    def test_optimized_sorts_match_corrected_and_are_stable(self) -> None:
        expected = [("a", 9), ("c", 9), ("b", 3), ("d", 3), ("e", 1)]
        for algorithm in (optimized.insertion_sort_alerts_instrumented, optimized.stable_merge_sort_alerts_instrumented):
            values = [("a", 9), ("b", 3), ("c", 9), ("d", 3), ("e", 1)]
            stats = algorithm(values)
            self.assertEqual(values, expected)
            self.assertGreaterEqual(stats.comparisons, 0)
            self.assertGreaterEqual(stats.movements, 0)
        for algorithm in (optimized.insertion_sort_alerts, optimized.stable_merge_sort_alerts):
            values = [("a", 9), ("b", 3), ("c", 9), ("d", 3), ("e", 1)]
            returned = algorithm(values)
            self.assertIs(returned, values)
            self.assertEqual(returned, expected)

    def test_sequential_search_boolean_convention_and_boundaries(self) -> None:
        self.assertTrue(corrected.is_blocked(SUPPLIED_BLOCKLIST, SUPPLIED_BLOCKLIST[0]))
        self.assertTrue(corrected.is_blocked(SUPPLIED_BLOCKLIST, SUPPLIED_BLOCKLIST[-1]))
        self.assertFalse(corrected.is_blocked(SUPPLIED_BLOCKLIST, "8.8.8.8"))
        self.assertFalse(corrected.is_blocked([], "10.0.0.5"))
        index = optimized.BlocklistIndex(SUPPLIED_BLOCKLIST)
        results, counts = index.query_many(["10.0.0.9", "10.0.0.5", "8.8.8.8", "10.0.0.9"])
        self.assertEqual(results, [True, True, False, True])
        self.assertEqual(counts.lookups, 4)

    def test_string_matching_supplied_and_all_boundaries(self) -> None:
        cases = [
            (SUPPLIED_LOG, "FAIL", [0, 8]),
            ("FAILxxx", "FAIL", [0]),
            ("xxxFAIL", "FAIL", [3]),
            ("ABABA", "ABA", [0, 2]),
            ("abc", "longer", []),
            ("abc", "", [0, 1, 2, 3]),
            ("", "", [0]),
            ("abc", "z", []),
        ]
        for log, pattern, expected in cases:
            with self.subTest(log=log, pattern=pattern):
                self.assertEqual(corrected.find_signature(log, pattern), expected)
                self.assertEqual(optimized.find_signature(log, pattern), expected)

    def test_optimized_string_comparison_counter(self) -> None:
        result = optimized.find_signature_instrumented("A" * 80, "A" * 20 + "B")
        self.assertEqual(result.positions, [])
        self.assertEqual(result.character_comparisons, (80 - 21 + 1) * 21)
        self.assertEqual(optimized.find_signature("ABABA", "ABA"), [0, 2])

    def test_corrected_closest_pair_supplied_and_known_answer(self) -> None:
        pair, distance = corrected.closest_logins(SUPPLIED_EVENTS)
        self.assertEqual(pair, (0, 5))
        self.assertAlmostEqual(distance, math.sqrt(2))
        known = [(0, 0), (3, 4), (1, 1)]
        pair, distance = corrected.closest_logins(known)
        self.assertEqual(pair, (0, 2))
        self.assertAlmostEqual(distance, math.sqrt(2))

    def test_closest_pair_duplicates_ties_negative_and_two_events(self) -> None:
        cases = [
            ([(0, 0), (0, 0), (3, 4)], (0, 1), 0.0),
            ([(0, 0), (1, 0), (0, 1)], (0, 1), 1.0),
            ([(-5, -5), (-4, -5), (20, 20)], (0, 1), 1.0),
            ([(1, 2), (4, 6)], (0, 1), 5.0),
        ]
        for events, expected_pair, expected_distance in cases:
            with self.subTest(events=events):
                self.assertEqual(corrected.closest_logins(events), (expected_pair, expected_distance))

    def test_closest_pair_rejects_small_inputs(self) -> None:
        for algorithm in (corrected.closest_logins, optimized.closest_logins_brute_force, optimized.closest_logins):
            for events in ([], [(1, 2)]):
                with self.subTest(algorithm=algorithm.__name__, events=events):
                    with self.assertRaises(ValueError):
                        algorithm(events)

    def test_brute_and_divide_conquer_closest_pair_agree(self) -> None:
        datasets = [
            SUPPLIED_EVENTS,
            [(index, (index * 17) % 31) for index in range(50)],
            [(0, 0), (2, 0), (0, 2), (2, 2), (1, 1)],
            [(-index, index * index % 23) for index in range(30)],
        ]
        for events in datasets:
            with self.subTest(size=len(events)):
                baseline = optimized.closest_logins_brute_force_instrumented(events)
                result = optimized.closest_logins_instrumented(events)
                self.assertEqual((result.pair, result.distance), (baseline.pair, baseline.distance))
                self.assertLessEqual(result.distance_calculations, result.candidate_pairs)
                self.assertEqual(optimized.closest_logins(events), corrected.closest_logins(events))
                self.assertEqual(optimized.closest_logins_brute_force(events), corrected.closest_logins(events))


class RecordingResult(unittest.TextTestResult):
    """Collect per-test outcomes as actual CSV evidence."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows: list[dict[str, str]] = []

    def _record(self, test: unittest.case.TestCase, status: str, detail: str = "") -> None:
        self.rows.append({"test": test.id(), "status": status, "detail": detail.replace("\n", " ")})

    def addSuccess(self, test):
        super().addSuccess(test)
        self._record(test, "PASS")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._record(test, "FAIL", self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        self._record(test, "ERROR", self._exc_info_to_string(err, test))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._record(test, "SKIP", reason)


class RecordingRunner(unittest.TextTestRunner):
    resultclass = RecordingResult


def main() -> None:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SentinelOpsTests)
    transcript = io.StringIO()
    result = RecordingRunner(verbosity=2, stream=transcript).run(suite)
    result_path = PROJECT_ROOT / "Supporting_Files" / "test_results.csv"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    with result_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("test", "status", "detail"))
        writer.writeheader()
        writer.writerows(result.rows)
    output_path = PROJECT_ROOT / "Output_Screenshots" / "benchmark_outputs" / "test_harness_output.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(transcript.getvalue(), encoding="utf-8")
    print(transcript.getvalue(), end="")
    sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    main()
