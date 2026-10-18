# Task 8 — Implement and test

The implementations are in [search_algorithms.py](search_algorithms.py):
an iterative scan, recursive binary search, and dictionary lookup. The source
returns the matching identifier or `None`; the same identifier can be
associated with a full student-record payload in a real system. Binary search
requires ascending input, while the other two strategies accept the shuffled
input used by the experiment.

The standard-library unit tests cover hits, misses, an empty input, and a
single-record input for each algorithm. Run them from the repository root:

```text
python -m unittest discover -s CO1_Assignment/Task_08_Implementation -p "test_*.py"
```

The benchmark uses deterministic shuffles and generated unique identifiers at
1,000, 10,000, 100,000, and 1,000,000 records. Each size uses the same 30
queries (15 present and 15 absent) for all three methods, validates each
result before timing, and records the median of five rounds. Sorting and
index-building are timed separately from lookup. Generation and correctness
checks are excluded from lookup timings. This is a reproducible synthetic
experiment, not a claim about production student data.
