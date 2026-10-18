# CO1 Assignment

Completed against the supplied original paper, which is included unchanged at
`Report/Reference/MALLAPU VIDYADHAR - CO1 ASSIGNMENT.pdf`. Each numbered task
has its own answer in the order and scope requested. The consolidated report
links all twelve answers and summarizes the measured evidence.

## Folder structure

```text
CO1_Assignment/
|-- Task_01_Algorithm_Design/answer.md
|-- Task_02_Basic_Operation/answer.md
|-- Task_03_Mathematical_Complexity/answer.md
|-- Task_04_Case_Analysis/answer.md
|-- Task_05_Asymptotic_Analysis/answer.md
|-- Task_06_Recurrence_Formulation/answer.md
|-- Task_07_Recurrence_Solution/answer.md
|-- Task_08_Implementation/
|   |-- search_algorithms.py
|   |-- test_search_algorithms.py
|   `-- run_benchmark.py
|-- Task_09_Performance_Analysis/
|   |-- performance.csv
|   `-- search_time.svg
|-- Task_10_Theory_Experiment/answer.md
|-- Task_11_Recommendation/answer.md
|-- Task_12_Design_Challenge/answer.md
`-- Report/
    |-- CO1_Assignment_Report.md
    |-- Reference/
    |-- Screenshots/Output/
    `-- Screenshots/Source_Code/
```

## Run and test

From the repository root, using Python 3.8 or newer:

```text
python -m unittest discover -s CO1_Assignment/Task_08_Implementation -p "test_*.py"
python CO1_Assignment/Task_08_Implementation/run_benchmark.py
```

The benchmark creates the measured CSV and SVG in Task 9. It deterministically
generates synthetic identifiers at the four required sizes, validates all
queries, and reports preprocessing separately from search time. It uses only
the Python standard library.

Screenshot directories are intentionally not populated with simulated
screenshots. Add genuine application-output and source-editor screenshots
there if required by the instructor. See the consolidated report for results,
limitations, and final manual-verification notes.
