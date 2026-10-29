"""Build the final DOCX report exclusively from verified CSVs and saved plots."""

from __future__ import annotations

import csv
import platform
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "Experimental_Data"
GRAPHS = ROOT / "Graphs"
REPORT = ROOT / "Final_Report" / "CO2_Assignment_Report.docx"


def load_rows(filename: str) -> list[dict[str, str]]:
    with (DATA / filename).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def add_page_number(section) -> None:
    paragraph = section.footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.add_run("CSA06 CO2 Assignment | Page ")
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    paragraph._p.append(field)


def add_table(document: Document, headers: list[str], rows: list[list[str]]) -> None:
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Light Shading Accent 1"
    for cell, text in zip(table.rows[0].cells, headers):
        cell.text = text
    for values in rows:
        cells = table.add_row().cells
        for cell, text in zip(cells, values):
            cell.text = str(text)
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(8)
    document.add_paragraph()


def add_figure(document: Document, filename: str, caption: str) -> None:
    path = GRAPHS / filename
    if path.exists():
        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.add_run().add_picture(str(path), width=Inches(6.2))
        caption_paragraph = document.add_paragraph(caption)
        caption_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        document.add_paragraph(f"Figure unavailable: {filename}")


def add_pseudocode(document: Document, relative_path: str) -> None:
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    code = text.split("```text", 1)[1].split("```", 1)[0].strip()
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.left_indent = Inches(0.25)
    run = paragraph.add_run(code)
    run.font.name = "Courier New"
    run.font.size = Pt(8)


def add_question_heading(document: Document, heading: str, marks: int) -> None:
    document.add_heading(f"{heading} ({marks} marks)", level=1)


def add_q1(document: Document) -> None:
    add_question_heading(document, "Q1. Sorting Under Different Data Conditions", 6)
    document.add_paragraph("Problem and design: sort dispatch scores using independent Selection, early-exit Bubble, and Insertion implementations. Each method receives a fresh copy. A swap is three element movements; Insertion counts each shift and key write. Predictions were recorded before measured results: Selection's comparisons depend only on n, while Insertion and early-exit Bubble should benefit on nearly ordered data.")
    document.add_paragraph("The 95% already-correct-order operating context makes Insertion Sort a plausible choice for small periodic batches, because shifting a few out-of-place items can be inexpensive. In the measured nearly-sorted case it used 54 comparisons versus Selection Sort's fixed 780. This experiment does not model every batch arrival pattern; actual batch size and the cost of integrating new orders determine the deployment choice. Selection Sort uses O(n^2) comparisons and O(1) auxiliary space. Bubble Sort is O(n) best case and O(n^2) average/worst, with O(1) extra space. Insertion Sort is O(n) best and O(n^2) average/worst, with O(1) extra space.")
    add_pseudocode(document, "Q1_Sorting_Algorithms/Pseudocode/sorting_pseudocode.md")
    rows = load_rows("q1_sorting_results.csv")
    add_table(document, ["Input", "Method", "n", "Comparisons", "Movements", "Seconds"], [[r["dataset"], r["algorithm"], r["n"], r["comparisons"], r["movements"], r["elapsed_seconds"]] for r in rows])
    add_figure(document, "q1_sorting_operations.png", "Figure 1. Measured comparisons and element movements.")
    document.add_paragraph("Conclusion: operation counts are the primary comparison evidence; these small timings are sensitive to runtime noise. The run log and CSV provide exact cases and correctness checks.")


def add_q2(document: Document) -> None:
    add_question_heading(document, "Q2. Sequential Search", 4)
    document.add_paragraph("Tool issue records contain tool ID, technician ID, issue time, and work bay. Search compares tool IDs in list order and returns the first matching record. A successful target at zero-based position p requires p+1 comparisons; a miss scans all n records. Best/average/worst time is O(1)/O(n)/O(n); auxiliary space is O(1). Sequential search is simple for small or infrequently queried unsorted collections. Frequent queries across 20 facilities may warrant a hash index, but building and maintaining that index costs time and memory and must be compared with the actual lookup workload.")
    add_pseudocode(document, "Q2_Sequential_Search/Pseudocode/sequential_search_pseudocode.md")
    rows = load_rows("q2_search_results.csv")
    add_table(document, ["n", "Case", "Target position", "Found", "Comparisons", "Correct"], [[r["n"], r["case"], r["target_position_zero_based"], r["found"], r["comparisons"], r["correct"]] for r in rows])
    document.add_paragraph("The deterministic record generator makes first, middle, final, and absent target behavior directly reproducible. The sequential lookup count excludes any preprocessing cost of alternative indexes.")


def add_q3(document: Document) -> None:
    add_question_heading(document, "Q3. Brute-Force String Matching", 6)
    document.add_paragraph("At each possible start offset the matcher compares characters left-to-right and stops that alignment at its first mismatch. It advances by one after a match, so overlaps are retained. The documented empty-pattern convention returns all n+1 text boundaries with zero comparisons; a pattern longer than the text has no matches and incurs zero comparisons. Positions are zero-based.")
    document.add_paragraph("Prediction: a repetitive text with a long matching prefix followed by a mismatch should approach the worst-case O((n-m+1)m) character comparisons for nonempty patterns, while an early easy match uses fewer. For n >= m this bound is O(nm). Length alone is insufficient to predict work because mismatch location and shared prefixes govern the comparisons per alignment.")
    add_pseudocode(document, "Q3_Brute_Force_String_Matching/Pseudocode/string_matching_pseudocode.md")
    rows = load_rows("q3_string_matching_results.csv")
    add_table(document, ["Case", "n", "m", "Zero-based matches", "Comparisons", "Validated"], [[r["case"], r["text_length"], r["pattern_length"], r["matches_zero_based"], r["character_comparisons"], r["correct"]] for r in rows])
    document.add_paragraph("Reported positions are independently checked using repeated standard-library find calls with a one-character increment, which allows overlapping matches.")


def add_q4(document: Document) -> None:
    add_question_heading(document, "Q4. Brute-Force Closest Pair", 6)
    document.add_paragraph("The nested loops use j > i, so every unordered pair is examined exactly once. There are (n-1)+(n-2)+...+1 = n(n-1)/2 pairs. Squared Euclidean distance is compared without square roots; one square root produces the final distance. Strict improvement preserves the first input-order pair on ties; duplicate coordinates yield distance zero. Fewer than two points raise ValueError.")
    document.add_paragraph("Time is O(n^2), auxiliary space O(1) excluding input storage. Before measurement the local acceptance criterion was set to 1.0 second per run. It is an environment-specific budget, not a universal hardware limit; the tested sizes establish only a local observation.")
    add_pseudocode(document, "Q4_Brute_Force_Closest_Pair/Pseudocode/closest_pair_pseudocode.md")
    rows = load_rows("q4_closest_pair_results.csv")
    add_table(document, ["n", "Expected pairs", "Measured pairs", "Distance calculations", "Seconds", "Within 1s"], [[r["n_points"], r["expected_pair_count"], r["actual_pair_count"], r["distance_calculations"], r["elapsed_seconds"], r["within_acceptance"]] for r in rows])
    add_figure(document, "q4_closest_pair_counts.png", "Figure 2. Theoretical pair counts coincide with measured pair counts.")
    document.add_paragraph("Observed local response boundary: n=3,000 completed in 0.662 s, while n=5,000 took 1.844 s and exceeded the predeclared 1.0-second budget. Thus the tested crossover lies between those sampled sizes for this environment and dataset generator; it is not a hardware-independent limit. A divide-and-conquer closest-pair strategy could avoid evaluating all pairs; this assignment measures the requested brute-force baseline.")


def add_q5(document: Document) -> None:
    add_question_heading(document, "Q5. Brute-Force Convex Hull", 7)
    document.add_paragraph("For A=(x1,y1), B=(x2,y2), P=(x3,y3), cross(A,B,P)=(x2-x1)(y3-y1)-(y2-y1)(x3-x1). Positive and negative signs indicate opposite sides of the directed line; zero means collinear. A candidate pair supports a hull line when all remaining points lie on one side or on the line. The implementation deduplicates coordinates, identifies the extremes of collinear boundary sets, handles fully collinear inputs, and angle-orders unique corners around their centroid. The angle-ordering argument assumes the identified set is the boundary of a convex polygon.")
    document.add_paragraph("The all-pairs/all-other-points approach is O(n^3) in the worst case; ordering h identified vertices costs O(h log h). A supporting line contains a convex-hull boundary segment because it separates all input points into a closed half-plane. Collinear points belong to an edge but only its two extremes are polygon corners.")
    add_pseudocode(document, "Q5_Brute_Force_Convex_Hull/Pseudocode/convex_hull_pseudocode.md")
    rows = load_rows("q5_convex_hull_results.csv")
    add_table(document, ["Configuration", "Input", "Unique", "Hull vertices", "Pairs", "Orientation tests", "Correct"], [[r["configuration"], r["input_count"], r["unique_points"], r["hull_vertices"], r["candidate_pairs"], r["orientation_tests"], r["correct"]] for r in rows])
    add_figure(document, "q5_boundary_and_interior.png", "Figure 3. Boundary and interior monitoring stations.")
    add_figure(document, "q5_collinear_duplicates_symmetric.png", "Figure 4. Duplicate, symmetric, and collinear boundary points.")


def add_q6(document: Document) -> None:
    add_question_heading(document, "Q6. Exhaustive Knapsack Search", 8)
    document.add_paragraph("Each bitmask represents one subset, including mask zero for the empty subset. For n packages there are 2^n masks. Each candidate is fully summed, and only feasible subsets compete for best value. Tie-breaking is maximum value, then lower weight, then lexicographically smaller sorted IDs. Positive weights, nonnegative values, unique IDs, and nonnegative capacity are validated. A three-package hand-check has optimum value 7 from weights 2 and 3 under capacity 5, independently verified in unit tests.")
    document.add_paragraph("The measured growth prediction is doubling per added package. The local response budget was set to 2.0 seconds before running the n=10, 15, and 20 cases. A practical limit may be inferred only for this environment and these instances; runtime also depends on implementation, package values/weights, and the available time budget. Adding k packages multiplies the subset count by 2^k.")
    add_pseudocode(document, "Q6_Exhaustive_Search/Pseudocode/exhaustive_search_pseudocode.md")
    rows = load_rows("q6_exhaustive_search_results.csv")
    add_table(document, ["n", "Capacity", "Subsets", "Feasible", "Best value", "Seconds", "Within budget"], [[r["n_packages"], r["capacity"], r["subsets_examined"], r["feasible_subsets"], r["best_value"], r["elapsed_seconds"], r["within_budget"]] for r in rows])
    add_figure(document, "q6_subset_growth.png", "Figure 5. Exhaustive subset counts grow exponentially.")
    document.add_paragraph("Observed local response boundary: n=19 completed in 1.065 s within the 2.0-second budget; n=20 took 2.190 s and exceeded it. The data therefore bracket the sampled transition between 19 and 20 packages on this machine and generated instances only. Because the instances are independently seeded by size, this is a practical observation, not a universal package-count guarantee.")


def add_q7(document: Document) -> None:
    add_question_heading(document, "Q7. Day-4 Design Challenge", 13)
    document.add_heading("A. Diagnose the bottleneck (2 marks)", level=2)
    document.add_paragraph("The baseline repeatedly evaluates complete subsets, with exactly 2^n candidates. In Q6, n=20 required 1,048,576 complete subsets and took 2.190 s, exceeding the declared 2.0-second budget; n=19 took 1.065 s. This exponential growth, rather than a single expensive arithmetic operation, is the limiting repeated work.")
    document.add_heading("B. Define the design objective (2 marks)", level=2)
    document.add_paragraph("Objective: reduce complete candidates considered while returning the same maximum value and a feasible package set on the same packages and capacity. Correctness requires matching the exhaustive optimum and respecting capacity; counts, preprocessing, memory, and elapsed time are reported separately.")
    document.add_heading("C. Design the revised strategy (4 marks)", level=2)
    document.add_paragraph("Branch-and-bound sorts items by value/weight ratio. A node stores its ordered index, weight, value, and original-index selection mask. The fractional-knapsack relaxation fills remaining capacity greedily and fractions the final item to produce a valid upper bound. Only a bound strictly below the current best value is pruned, preserving tie-break candidates. Nodes, expansions, and prunes are counted. The search uses O(n) recursion and ordering storage, plus O(n log n) preprocessing; worst-case time remains exponential, and equal-ratio instances may prune poorly.")
    add_pseudocode(document, "Q7_Day4_Design_Challenge/Pseudocode/redesigned_knapsack_pseudocode.md")
    document.add_heading("D. Predict before implementation (1 mark)", level=2)
    document.add_paragraph("Prediction recorded before running the redesigned comparison: diverse ratios will support effective pruning, while equal ratios will leave the fractional bound loose and approach exhaustive node counts.")
    document.add_heading("E. Implement and validate (2 marks)", level=2)
    rows = load_rows("q7_redesign_comparison.csv")
    add_table(document, ["Dataset", "n", "Exhaustive subsets", "BnB leaves", "BnB visited", "Pruned", "Original s", "BnB total s", "Same optimum"], [[r["dataset"], r["n_packages"], r["original_candidate_subsets"], r["bnb_complete_subsets_evaluated"], r["bnb_visited_nodes"], r["bnb_pruned_nodes"], r["original_elapsed_seconds"], r["bnb_total_seconds"], r["correct"]] for r in rows])
    add_figure(document, "q7_search_effort.png", "Figure 6. Search effort on identical original and redesigned instances.")
    document.add_paragraph("Both methods receive the same generated packages and capacity in each row. Output IDs are checked against the input set and both weights against capacity; values must agree.")
    document.add_heading("F. Defend the final design (2 marks)", level=2)
    for row in rows:
        leaf_reduction = 100 * float(row["complete_candidate_reduction_fraction"])
        original_time = float(row["original_elapsed_seconds"])
        redesigned_time = float(row["bnb_total_seconds"])
        speedup = original_time / redesigned_time if redesigned_time else float("inf")
        document.add_paragraph(f"{row['dataset']}: BnB evaluated {row['bnb_complete_subsets_evaluated']} complete leaves versus {row['original_candidate_subsets']} exhaustive subsets ({leaf_reduction:.1f}% fewer complete candidates), visited {row['bnb_visited_nodes']} total nodes, and pruned {row['bnb_pruned_nodes']} nodes. One measured run took {original_time:.6f}s exhaustive and {redesigned_time:.6f}s including BnB preprocessing (observed ratio {speedup:.1f}x). In the equal-ratio case, BnB visited more total nodes than there are baseline subsets despite evaluating fewer leaves, illustrating weak pruning and per-node overhead. Timing ratios from tiny single runs are noisy; the candidate counts are stronger evidence. BnB remains exponential in the worst case, and exhaustive search remains competitive for sufficiently small n.")


def main() -> None:
    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    add_page_number(section)
    styles = document.styles
    styles["Normal"].font.name = "Aptos"
    styles["Normal"].font.size = Pt(10)

    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run("CSA06\nDESIGN AND ANALYSIS OF ALGORITHMS").bold = True
    title.runs[0].font.size = Pt(20)
    document.add_paragraph("Assignment 2 | Course Outcome 2", style="Subtitle").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph("Brute-Force Sorting, Searching, Geometry, and Exact Search", style="Title").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph("Individual Assignment | Total: 50 marks | Python 3", style="Subtitle").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph(f"Evidence generated on {platform.platform()} with Python {platform.python_version()}.").alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_page_break()

    document.add_heading("Contents", level=1)
    for item in ("Objectives and methodology", "Q1 Sorting (6)", "Q2 Sequential search (4)", "Q3 String matching (6)", "Q4 Closest pair (6)", "Q5 Convex hull (7)", "Q6 Exhaustive knapsack (8)", "Q7 Day-4 redesign (13)", "Overall conclusions", "Viva preparation"):
        document.add_paragraph(item, style="List Bullet")
    document.add_heading("Objectives and Methodology", level=1)
    document.add_paragraph("The assignment applies brute-force techniques to sorting, searching, string matching, closest pair, convex hull, and knapsack, then evaluates an exact branch-and-bound redesign. Each experiment follows Predict, Design, Implement, Measure, Analyse, Evaluate, Diagnose, Redesign, Validate. Deterministic datasets, explicit operation counters, independent correctness checks, CSV source data, and saved plots support reproducibility. Timings use time.perf_counter; small timings are noisy and environment-specific.")
    document.add_paragraph("Measurement environment: " + platform.platform() + f"; Python {platform.python_version()}. Values in the tables are read from the generated CSV files. The Q1–Q7 execution_output.txt files are program logs, not screenshots. A terminal capture procedure is documented in the README.")

    add_q1(document)
    add_q2(document)
    add_q3(document)
    add_q4(document)
    add_q5(document)
    add_q6(document)
    add_q7(document)

    document.add_heading("Overall Conclusions", level=1)
    document.add_paragraph("Elementary algorithms remain useful when inputs are small or structurally favorable: insertion sort fits nearly ordered batches, sequential search fits small unsorted records, and brute-force geometric methods provide auditable baselines. Their operation counts expose where input structure matters. Exhaustive knapsack is exact but scales as 2^n; fractional-bound branch-and-bound reduced search on favorable instances while retaining exponential worst-case behavior. Choose a method from the measured workload and resource budget rather than a universal timing threshold.")
    document.add_heading("Viva Preparation", level=1)
    viva = [
        ("Why does insertion sort perform well on nearly sorted input?", "Its shifts are proportional to inversions; a small number of displaced items causes relatively little work."),
        ("Why does selection sort still make many comparisons on sorted data?", "It scans the remaining suffix to find each minimum regardless of input order."),
        ("Why does a sequential-search miss take n comparisons?", "Every record must be ruled out in the absence of an index."),
        ("How are overlapping string matches found?", "The next alignment starts one position later, not after the matched pattern."),
        ("Why compare squared distances?", "Squaring preserves nonnegative distance order and avoids repeated square roots."),
        ("What does a zero orientation determinant mean?", "The three points are collinear."),
        ("How many unordered pairs are there among n points?", "n(n-1)/2, by summing the inner-loop lengths."),
        ("Why include the empty knapsack subset?", "It is always feasible for nonnegative capacity and establishes value zero as a baseline."),
        ("Why is the fractional bound valid?", "Allowing a fraction of an item relaxes the 0/1 constraint, so the relaxed optimum cannot be below the 0/1 optimum."),
        ("Does branch-and-bound guarantee polynomial time?", "No. Its worst case remains exponential when the bound cannot prune enough."),
        ("Why are operation counts useful alongside timing?", "They are less sensitive to machine load and expose the algorithm's measured work."),
        ("When could a hash table improve sequential lookup?", "With frequent repeated lookups, if indexing/maintenance and memory costs are justified by the workload."),
    ]
    for question, answer in viva:
        paragraph = document.add_paragraph()
        paragraph.add_run("Q: " + question + " ").bold = True
        paragraph.add_run("A: " + answer)
    document.add_heading("References", level=1)
    document.add_paragraph("No external algorithmic sources were consulted. Definitions, pseudocode, and complexity arguments are presented as part of this assignment; measured results are generated by the included code.")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    document.save(REPORT)
    print(f"Generated {REPORT}")


if __name__ == "__main__":
    main()
