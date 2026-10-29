# CSA06 Design and Analysis of Algorithms — Assignment 2 (CO2)

**Course outcome:** Apply brute-force techniques to sorting, searching, closest-pair, convex-hull, and exhaustive-search problems.  
**Language:** Python 3  
**Marks:** 50  
**Root:** `CO2_Assignment/` (this directory; it is not nested inside another CO2 folder)

This assignment follows **Predict → Design → Implement → Measure → Analyse → Evaluate → Diagnose → Redesign → Validate**. Every benchmark is generated from code, every CSV is produced by `run_experiments.py`, and the report reads its result tables and figures from those generated artifacts.

## Setup

Install Python 3.10 or later. From the workspace root:

```powershell
py -m venv CO2_Assignment/.venv
CO2_Assignment\.venv\Scripts\python.exe -m pip install -r CO2_Assignment/requirements.txt
```

Linux/macOS equivalent:

```sh
python3 -m venv CO2_Assignment/.venv
CO2_Assignment/.venv/bin/python -m pip install -r CO2_Assignment/requirements.txt
```

The only third-party dependencies are Matplotlib (plots) and `python-docx` (the final report). The algorithm code and tests use the Python standard library.

## Run the assignment

From the workspace root, run an individual implementation demo:

```text
python -m CO2_Assignment.Q1_Sorting_Algorithms.Implementation_Code.sorting_algorithms
python -m CO2_Assignment.Q2_Sequential_Search.Implementation_Code.sequential_search
python -m CO2_Assignment.Q3_Brute_Force_String_Matching.Implementation_Code.brute_force_string_matching
python -m CO2_Assignment.Q4_Brute_Force_Closest_Pair.Implementation_Code.brute_force_closest_pair
python -m CO2_Assignment.Q5_Brute_Force_Convex_Hull.Implementation_Code.brute_force_convex_hull
python -m CO2_Assignment.Q6_Exhaustive_Search.Implementation_Code.exhaustive_knapsack
python -m CO2_Assignment.Q7_Day4_Design_Challenge.Implementation_Code.design_challenge
```

Regenerate every measured CSV, graph, and per-question output log, then build the DOCX report:

```text
python -m CO2_Assignment.run_experiments
python -m CO2_Assignment.build_report
```

Run unit tests:

```text
python -m unittest discover -s CO2_Assignment/tests -v
```

## Repository map

- `Q1_Sorting_Algorithms/` — Selection, early-exit Bubble, and Insertion Sort; comparison/movement CSV and graph.
- `Q2_Sequential_Search/` — deterministic tool issue records and position-sensitive comparison counts.
- `Q3_Brute_Force_String_Matching/` — all occurrences, overlap handling, explicit character comparisons.
- `Q4_Brute_Force_Closest_Pair/` — unique unordered-pair scan and measured/theoretical count graph.
- `Q5_Brute_Force_Convex_Hull/` — supporting-line hull, duplicate and collinear handling, and two plotted configurations.
- `Q6_Exhaustive_Search/` — complete bitmask enumeration, including the empty subset.
- `Q7_Day4_Design_Challenge/` — exact fractional-bound branch-and-bound comparison with exhaustive search.
- `Experimental_Data/` — seven measured CSV files; these are the data source for the report.
- `Graphs/` — generated Q1, Q4, Q5, Q6, and Q7 figures.
- `Final_Report/CO2_Assignment_Report.docx` — consolidated report with CSV-driven tables and figures.
- `tests/` — edge and correctness tests.

## Algorithm summary

| Question | Algorithm | Time | Extra space |
|---|---|---|---|
| Q1 | Selection Sort | Θ(n²) | O(1) |
| Q1 | Early-exit Bubble Sort | O(n) best; O(n²) average/worst | O(1) |
| Q1 | Insertion Sort | O(n) best; O(n²) average/worst | O(1) |
| Q2 | Sequential Search | O(1) best; O(n) average/worst | O(1) |
| Q3 | Brute-force matching | O((n-m+1)m) worst case | O(1) excluding matches |
| Q4 | Closest pair | O(n²) | O(1) excluding input |
| Q5 | Supporting-line convex hull | O(n³) worst case | O(n) boundary storage |
| Q6 | Exhaustive 0/1 knapsack | O(n·2^n) | O(n) per subset |
| Q7 | Branch-and-bound 0/1 knapsack | Exponential worst case | O(n) recursion/order storage |

Q1 compares identical inputs on independent copies; movements are explicitly defined in its pseudocode. Q4 accepts 2+ points and keeps the first pair on tied minima. Q5 returns only hull-corner extremes when an edge has intermediate collinear points. Q6/Q7 require unique IDs, positive weights, nonnegative values, and nonnegative capacity; their deterministic tie-break is maximum value, then lower weight, then lexical IDs.

## Experiment design and limits

The data generator uses deterministic descriptions/seeds, `time.perf_counter()`, explicit operation counts, and correctness assertions. Q4 uses n=10, 100, 500 with a locally stated 1.0-second acceptance budget. Q6 uses n=10, 15, 20 and a locally stated 2.0-second budget. These thresholds are evaluation criteria for this environment, not universal hardware limits. Q7 includes both diverse-ratio and equal-ratio instances; the latter demonstrates that the bound may prune poorly. Small timing differences are noisy, so operation counts are the primary evidence.

No numerical boundary is inferred beyond the tested instances. Q1's nearly sorted experiment is evidence for a candidate, not a full simulation of 95% of fulfilment orders arriving in all possible batch patterns. Q7 remains exponential in the worst case.

## Output evidence and screenshots

The `Output_Screenshots/` folders contain `execution_output.txt` files captured directly from the experiment runner. They are genuine program-output logs, **not screenshots**. This environment does not provide a terminal screenshot capture tool. To create a manual screenshot in VS Code on Windows:

1. Open the workspace root in VS Code and run the matching module command above in the integrated terminal.
2. Expand the terminal so the question identity, input description, results, and counters are readable.
3. Press `Win+Shift+S`, capture the terminal, and save the image in that question's `Output_Screenshots/` folder as `manual_terminal_capture.png`.
4. For Q5, the actual Matplotlib hull images are already in `Graphs/`; these graph images are not represented as terminal screenshots.

## Validation and deliverables

Run `python -m unittest discover -s CO2_Assignment/tests -v`, then regenerate experiments and report. CSV rows include correctness flags and the report embeds the values read from those CSVs. The included checks cover edge cases and an independently hand-verifiable knapsack optimum.

The report is generated as `Final_Report/CO2_Assignment_Report.docx`. It contains structured contents, problem designs, pseudocode, measured result tables, plots, complexity notes, Q7's six required sections, conclusions, and viva questions. No external algorithmic sources were consulted.

Remaining manual task: capture and add the seven terminal screenshots using the procedure above if actual image screenshots are required by the instructor. No Git history, remote, or unrelated CO1 content is changed by this CO2 package.
