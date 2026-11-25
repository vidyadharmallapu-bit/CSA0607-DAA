import os
import pathlib

base = pathlib.Path(r"c:\Users\vidya\OneDrive\Documents\Desktop\CSA0607-DAA\CSA06-Assignment-3")

# Create main directories
dirs = [
    base / "Q1",
    base / "Q2",
    base / "Q3",
    base / "Q4",
    base / "Q5",
    base / "Q6",
    base / "Q7",
    base / "experiments",
    base / "docs",
]

for d in dirs:
    d.mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {d}")

# Create all the file paths
files = {}

# Root level files
root_files = ["README.md", "requirements.txt", ".gitignore"]
for f in root_files:
    filepath = base / f
    files[f] = filepath
    # Create empty file if it doesn't exist
    if not filepath.exists():
        filepath.touch()
        print(f"Created file: {f}")

# Q1 files
q1_dir = base / "Q1"
q1_files = ["max_min.py", "binary_search.py", "README.md"]
for f in q1_files:
    files[f] = q1_dir / f
    if not filepath.exists():
        filepath.touch()

# Q2 files
q2_dir = base / "Q2"
q2_files = ["merge_sort.py", "quick_sort.py", "README.md"]
for f in q2_files:
    files[f] = q2_dir / f
    if not filepath.exists():
        filepath.touch()

# Q3 files
q3_dir = base / "Q3"
q3_files = ["standard_multiplication.py", "karatsuba.py", "README.md"]
for f in q3_files:
    files[f] = q3_dir / f
    if not filepath.exists():
        filepath.touch()

# Q4 files
q4_dir = base / "Q4"
q4_files = ["conventional_matrix.py", "strassen.py", "README.md"]
for f in q4_files:
    files[f] = q4_dir / f
    if not filepath.exists():
        filepath.touch()

# Q5 files
q5_dir = base / "Q5"
q5_files = ["brute_force.py", "closest_pair.py", "README.md"]
for f in q5_files:
    files[f] = q5_dir / f
    if not filepath.exists():
        filepath.touch()

# Q6 files
q6_dir = base / "Q6"
q6_files = ["median_of_medians.py", "quickselect.py", "meet_in_middle.py", "README.md"]
for f in q6_files:
    files[f] = q6_dir / f
    if not filepath.exists():
        filepath.touch()

# Q7 files
q7_dir = base / "Q7"
files["solution.py"] = q7_dir / "solution.py"
files["README.md"] = q7_dir / "README.md"  # This will overlap, handle later
if not (q7_dir / "solution.py").exists():
    (q7_dir / "solution.py").touch()
if not (q7_dir / "README.md").exists():
    (q7_dir / "README.md").touch()

# Experiments files
exp_dir = base / "experiments"
if not (exp_dir / "benchmark_results.csv").exists():
    (exp_dir / "benchmark_results.csv").touch()

# Docs files
docs_dir = base / "docs"
if not (docs_dir / "mathematical_analysis.md").exists():
    (docs_dir / "mathematical_analysis.md").touch()
if not (docs_dir / "contribution_record.md").exists():
    (docs_dir / "contribution_record.md").touch()

print("\nAll directories and empty files created successfully!")
print(f"Base repository: {base}")