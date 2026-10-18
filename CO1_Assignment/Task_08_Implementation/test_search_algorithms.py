import unittest

from search_algorithms import hash_search, linear_search, recursive_binary_search


class SearchAlgorithmTests(unittest.TestCase):
    def setUp(self):
        self.unsorted_records = ["STU0000003", "STU0000001", "STU0000002"]
        self.sorted_records = sorted(self.unsorted_records)
        self.index = {record: record for record in self.unsorted_records}

    def test_finds_existing_records(self):
        for record in self.unsorted_records:
            with self.subTest(record=record):
                self.assertEqual(linear_search(self.unsorted_records, record), record)
                self.assertEqual(recursive_binary_search(self.sorted_records, record), record)
                self.assertEqual(hash_search(self.index, record), record)

    def test_returns_none_for_missing_record(self):
        target = "STU9999999"
        self.assertIsNone(linear_search(self.unsorted_records, target))
        self.assertIsNone(recursive_binary_search(self.sorted_records, target))
        self.assertIsNone(hash_search(self.index, target))

    def test_handles_empty_input(self):
        self.assertIsNone(linear_search([], "STU0000001"))
        self.assertIsNone(recursive_binary_search([], "STU0000001"))
        self.assertIsNone(hash_search({}, "STU0000001"))

    def test_handles_single_record(self):
        records = ["STU0000001"]
        index = {records[0]: records[0]}
        self.assertEqual(linear_search(records, records[0]), records[0])
        self.assertEqual(recursive_binary_search(records, records[0]), records[0])
        self.assertEqual(hash_search(index, records[0]), records[0])
        self.assertIsNone(recursive_binary_search(records, "STU0000002"))


if __name__ == "__main__":
    unittest.main()
