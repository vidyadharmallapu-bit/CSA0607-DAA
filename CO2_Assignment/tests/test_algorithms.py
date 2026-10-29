import unittest
import random

from CO2_Assignment.Q1_Sorting_Algorithms.Implementation_Code.sorting_algorithms import SORTS
from CO2_Assignment.Q2_Sequential_Search.Implementation_Code.sequential_search import make_records, sequential_search
from CO2_Assignment.Q3_Brute_Force_String_Matching.Implementation_Code.brute_force_string_matching import brute_force_match
from CO2_Assignment.Q4_Brute_Force_Closest_Pair.Implementation_Code.brute_force_closest_pair import closest_pair
from CO2_Assignment.Q5_Brute_Force_Convex_Hull.Implementation_Code.brute_force_convex_hull import convex_hull
from CO2_Assignment.Q6_Exhaustive_Search.Implementation_Code.exhaustive_knapsack import Package, exhaustive_knapsack
from CO2_Assignment.Q7_Day4_Design_Challenge.Implementation_Code.design_challenge import branch_and_bound_knapsack


class AlgorithmTests(unittest.TestCase):
    def test_sorts_cover_empty_single_and_duplicates(self):
        for sort in SORTS.values():
            for source in ([], [1], [4, 1, 4, -2]):
                values = source.copy()
                stats = sort(values)
                self.assertEqual(values, sorted(source))
                self.assertGreaterEqual(stats.comparisons, 0)

    def test_sequential_search_positions_and_miss(self):
        records = make_records(5)
        self.assertEqual(sequential_search(records, "T00000"), (0, 1))
        self.assertEqual(sequential_search(records, "T00002"), (2, 3))
        self.assertEqual(sequential_search(records, "T00004"), (4, 5))
        self.assertEqual(sequential_search(records, "missing"), (None, 5))

    def test_string_matching_overlaps_empty_and_long_pattern(self):
        self.assertEqual(brute_force_match("AAAA", "AA"), ([0, 1, 2], 6))
        self.assertEqual(brute_force_match("abc", ""), ([0, 1, 2, 3], 0))
        self.assertEqual(brute_force_match("a", "long"), ([], 0))

    def test_closest_pair_duplicate_tie_and_invalid_input(self):
        duplicate = closest_pair([(0, 0), (1, 0), (0, 0)])
        self.assertEqual(duplicate.distance, 0)
        self.assertEqual((duplicate.first, duplicate.second), ((0, 0), (0, 0)))
        tied = closest_pair([(0, 0), (1, 0), (0, 1)])
        self.assertEqual(tied.pairs_examined, 3)
        self.assertEqual((tied.first, tied.second), ((0, 0), (1, 0)))
        with self.assertRaises(ValueError):
            closest_pair([(1, 1)])

    def test_convex_hull_degenerate_duplicate_and_collinear(self):
        self.assertEqual(convex_hull([]).vertices, [])
        self.assertEqual(convex_hull([(2, 2), (2, 2)]).vertices, [(2, 2)])
        self.assertEqual(convex_hull([(2, 2), (0, 0)]).vertices, [(0, 0), (2, 2)])
        self.assertEqual(convex_hull([(0, 0), (1, 1), (2, 2)]).vertices, [(0, 0), (2, 2)])
        result = convex_hull([(0, 0), (1, 0), (2, 0), (2, 2), (0, 2), (1, 1), (0, 0)])
        self.assertEqual(len(result.vertices), 4)
        self.assertNotIn((1, 0), result.vertices)
        self.assertNotIn((1, 1), result.vertices)

    def test_exhaustive_and_branch_bound_match_small_optimum(self):
        packages = [Package("A", 2, 3), Package("B", 3, 4), Package("C", 4, 5)]
        exhaustive = exhaustive_knapsack(packages, 5)
        redesigned = branch_and_bound_knapsack(packages, 5)
        self.assertEqual(exhaustive.total_value, 7)
        self.assertEqual(exhaustive.total_value, redesigned.total_value)
        self.assertLessEqual(exhaustive.total_weight, 5)
        self.assertLessEqual(redesigned.total_weight, 5)
        self.assertEqual(exhaustive.subsets_examined, 8)
        self.assertEqual(exhaustive.package_ids, ("A", "B"))
        self.assertEqual(exhaustive.total_weight, 5)

    def test_knapsack_empty_and_seeded_differential_instances(self):
        self.assertEqual(exhaustive_knapsack([], 0).package_ids, ())
        rng = random.Random(711)
        for case in range(12):
            packages = [Package(f"P{case}_{index}", rng.randint(1, 9), rng.randint(0, 15)) for index in range(case % 8)]
            capacity = rng.randint(0, 20)
            exhaustive = exhaustive_knapsack(packages, capacity)
            redesigned = branch_and_bound_knapsack(packages, capacity)
            self.assertEqual((redesigned.total_value, redesigned.total_weight, redesigned.package_ids), (exhaustive.total_value, exhaustive.total_weight, exhaustive.package_ids))


if __name__ == "__main__":
    unittest.main()