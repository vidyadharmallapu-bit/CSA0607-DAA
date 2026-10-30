# CO₂ Assessment Tool 2: Debugging and Optimization

**Department:** Computer Science and Engineering  
**Course:** CSA06 — Design and Analysis of Algorithms  
**Assessment:** CO2 debugging and optimization  
**Scenario:** SentinelOps SOC alert triage  
**Maximum marks:** 50  
**Language:** Python 3

This standalone project preserves the supplied faulty implementation, reproduces its actual results, corrects the four routines with traceable changes, and compares justified optimizations against the corrected baseline. It is located in `CO_2_Assessment_Tool_2_Debugging_and_Optimization/`, alongside rather than inside the other assignments.

## Setup

Install Python 3.10 or later. From the workspace root on Windows:

```powershell
py -m venv CO_2_Assessment_Tool_2_Debugging_and_Optimization/.venv
CO_2_Assessment_Tool_2_Debugging_and_Optimization\.venv\Scripts\python.exe -m pip install -r CO_2_Assessment_Tool_2_Debugging_and_Optimization/requirements.txt
```

Linux/macOS:

```sh
python3 -m venv CO_2_Assessment_Tool_2_Debugging_and_Optimization/.venv
CO_2_Assessment_Tool_2_Debugging_and_Optimization/.venv/bin/python -m pip install -r CO_2_Assessment_Tool_2_Debugging_and_Optimization/requirements.txt
```

Algorithms and tests use the standard library. Matplotlib and `python-docx` are used only for graphs and the report.

## Run and reproduce

Run the original-vs-corrected-vs-optimized demonstrations, insertion trace, and all string alignments:

```text
python -m CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code.debug_trace
```

Run all unit tests. The command exits nonzero on any failure and writes `Supporting_Files/test_results.csv` plus a console transcript:

```text
python -m CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code.test_harness
```

Regenerate every benchmark CSV, graph, and benchmark log:

```text
python -m CO_2_Assessment_Tool_2_Debugging_and_Optimization.Source_Code.benchmark
```

Build the Word report from the regenerated evidence:

```text
python -m CO_2_Assessment_Tool_2_Debugging_and_Optimization.build_report
```

## Structure

- `Source_Code/original_faulty_module.py` — supplied logic preserved for audit.
- `Source_Code/corrected_module.py` — minimal corrected algorithms.
- `Source_Code/optimized_module.py` — public optimized functions preserve corrected return types; separately named `*_instrumented` variants expose sorting, matching, and closest-pair counters for benchmarking. Includes reusable blocklist set, brute closest-pair baseline, and exact divide-and-conquer method.
- `Source_Code/debug_trace.py` — actual original/corrected/optimized outputs and detailed traces.
- `Source_Code/test_harness.py` — standard-library regression tests with CSV result output.
- `Source_Code/benchmark.py` — reproducible experiments, CSVs, graphs, and output log.
- `Pseudocode/` — four algorithm listings.
- `Supporting_Files/defect_register.md` — nine primary defect categories and the count ambiguity.
- `Supporting_Files/debugging_log.md` — observed failures, fixes, and corrected results.
- `Supporting_Files/complexity_analysis.md` — original, corrected, and optimized complexity analysis.
- `Supporting_Files/test_datasets.json` — supplied fixtures, seeds, and sizes.
- `Supporting_Files/*_benchmarks.csv` — actual measured rows; graphs read these CSVs.
- `Supporting_Files/graphs/` — generated comparison graphs.
- `Report/SentinelOps_Debugging_Optimisation_Report.docx` — final report generated from CSV data and saved graphs.
- `Output_Screenshots/` — genuine terminal output logs grouped by original, corrected, optimized, and benchmark runs.

## Defect summary

The expected nine primary categories are supported by the source: (1) insertion-sort scan/placement indices, (2) blocked-hit returns false, (3) miss branch exits on the first nonmatch, (4) string alignment bound omits the final start, (5) empty pattern reads uninitialized `j`, (6) match detection accepts a last-character mismatch, (7) closest-pair best distance starts at zero, (8) distance comparison maximizes rather than minimizes, and (9) pair loops include self-pairs and duplicate orientations. The sorting category includes two related bad index expressions; the register explains why the assignment-level category count is nine while a statement-level count is ten.

## Complexity and design notes

| Routine | Corrected baseline | Optimized version |
|---|---|---|
| Alert sort | Stable insertion O(n) best, O(n²) average/worst, O(1) space | Stable merge O(n log n), O(n) space; insertion retained for nearly-sorted small batches |
| Blocklist | Sequential O(n) per query | Set construction O(n) expected, O(1) expected lookup; hash worst case is not guaranteed constant |
| Signature match | Brute force O((n-m+1)m) worst | Counted brute force reduces no asymptotic bound; early mismatch and overlap-safe |
| Closest pair | Unique-pair brute force Θ(n²), O(1) extra space | Exact divide-and-conquer O(n log n), O(n) auxiliary space |

Squared distances avoid repeated square roots but do not reduce brute-force candidate count. The divide-and-conquer strip bound is exact; duplicates are handled before recursion to preserve zero-distance results and deterministic ties. Dataset seeds and timing environment are recorded in CSVs. Instrumentation affects runtime, so operation counts are shown separately from timing.

## Results snapshot

The supplied original code returned corrupted sort contents, false for all three IP queries, signature starts `[0, 4]`, and the farthest pair `(0, 2)` at `60.440052945046 km`; empty pattern raised `UnboundLocalError`. Corrected results are stable descending alerts, `[True, True, False]`, signature positions `[0, 8]`, and pair `(0, 5)` at `sqrt(2) km`.

At n=8,000, the brute closest-pair baseline measured 31,996,000 distance calculations; divide-and-conquer measured 9,336 with the same exact pair and distance. Sorting benchmarks show insertion is effective for nearly sorted input, while the stable merge alternative outperformed insertion on random/reverse data at larger n. Consult CSVs for the complete measured values.

## Evidence and screenshots

The `Output_Screenshots/` tree currently contains unaltered program output logs, not screenshots. Automated terminal screenshot capture is unavailable here. To add instructor-ready genuine screenshots on Windows, run each command above in the VS Code integrated terminal, widen the terminal so the command identity and relevant results are readable, press `Win+Shift+S`, and save the capture in the matching folder (for example `Output_Screenshots/benchmark_outputs/closest_pair_capture.png`). The generated Matplotlib figures are actual graphs, not terminal screenshots.

## Limitations

Timings were measured in one Linux container with Python 3.14.2 and are not Windows performance promises. Random coordinate tests use deterministic seeds and finite continuous coordinates. Hash-table constant-time lookup is expected rather than a worst-case guarantee. The nine-entry defect register groups the sort's two related index mistakes as one assignment category and discloses the statement-level count.
