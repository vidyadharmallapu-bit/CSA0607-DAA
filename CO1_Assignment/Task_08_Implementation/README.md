# Task 8 — Implementation and tests

`search_algorithms.py` contains the three approaches analysed in Tasks 1–7.
`test_search_algorithms.py` checks hits, misses, empty input and a one-record
input using Python's standard library. `run_benchmark.py` performs the
reproducible experiment and writes measured CSV/SVG results to Task 9.

From the repository root, run:

```text
python -m unittest discover -s CO1_Assignment/Task_08_Implementation -p "test_*.py"
python CO1_Assignment/Task_08_Implementation/run_benchmark.py
```

Python 3.8 or newer is recommended. No third-party package is required by the
implementation, tests or benchmark.
