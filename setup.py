import os

base = r"c:\Users\vidya\OneDrive\Documents\Desktop\CSA0607-DAA\CSA06-Assignment-3"

# Create main directories
dirs = [
    base + "\Q1",
    base + "\Q2",
    base + "\Q3",
    base + "\Q4",
    base + "\Q5",
    base + "\Q6",
    base + "\Q7",
    base + "\experiments",
    base + "\docs",
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print("Created directory: " + d)

# Create root level files
root_files = ["README.md", "requirements.txt", ".gitignore"]
for f in root_files:
    filepath = base + "\\" + f
    if not os.path.exists(filepath):
        with open(filepath, "w") as fh:
            fh.write("")
        print("Created file: " + f)

# Q1 files
q1_dir = base + "\Q1"
q1_files = ["max_min.py", "binary_search.py", "README.md"]
for f in q1_files:
    filepath = q1_dir + "\\" + f
    if not os.path.exists(filepath):
        with open(filepath, "w") as fh:
            fh.write("")
    print("Created file: Q1\\" + f)

# Q2 files
q2_dir = base + "\Q2"
q2_files = ["merge_sort.py", "quick_sort.py", "README.md"]
for f in q2_files:
    filepath = q2_dir + "\\" + f
    if not os.path.exists(filepath):
        with open(filepath, "w") as fh:
            fh.write("")
    print("Created file: Q2\\" + f)

# Q3 files
q3_dir = base + "\Q3"
q3_files = ["standard_multiplication.py", "karatsuba.py", "README.md"]
for f in q3_files:
    filepath = q3_dir + "\\" + f
    if not os.path.exists(filepath):
        with open(filepath, "w") as fh:
            fh.write("")
    print("Created file: Q3\\" + f)

# Q4 files
q4_dir = base + "\Q4"
q4_files = ["conventional_matrix.py", "strassen.py", "README.md"]
for f in q4_files:
    filepath = q4_dir + "\\" + f
    if not os.path.exists(filepath):
        with open(filepath, "w") as fh:
            fh.write("")
    print("Created file: Q4\\" + f)

# Q5 files
q5_dir = base + "\Q5"
q5_files = ["brute_force.py", "closest_pair.py", "README.md"]
for f in q5_files:
    filepath = q5_dir + "\\" + f
    if not os.path.exists(filepath):
        with open(filepath, "w") as fh:
            fh.write("")
    print("Created file: Q5\\" + f)

# Q6 files
q6_dir = base + "\Q6"
q6_files = ["median_of_medians.py", "quickselect.py", "meet_in_middle.py", "README.md"]
for f in q6_files:
    filepath = q6_dir + "\\" + f
    if not os.path.exists(filepath):
        with open(filepath, "w") as fh:
            fh.write("")
    print("Created file: Q6\\" + f)

# Q7 files
q7_dir = base + "\Q7"
if not os.path.exists(q7_dir + "\solution.py"):
    with open(q7_dir + "\solution.py", "w") as fh:
        fh.write("")
print("Created file: Q7\\solution.py")
if not os.path.exists(q7_dir + "\README.md"):
    with open(q7_dir + "\README.md", "w") as fh:
        fh.write("")
print("Created file: Q7\\README.md")

# Experiments files
exp_dir = base + "\experiments"
if not os.path.exists(exp_dir + "\benchmark_results.csv"):
    with open(exp_dir + "\benchmark_results.csv", "w") as fh:
        fh.write("")
print("Created file: experiments\\benchmark_results.csv")

# Docs files
docs_dir = base + "\docs"
if not os.path.exists(docs_dir + "\mathematical_analysis.md"):
    with open(docs_dir + "\mathematical_analysis.md", "w") as fh:
        fh.write("")
print("Created file: docs\\mathematical_analysis.md")
if not os.path.exists(docs_dir + "\contribution_record.md"):
    with open(docs_dir + "\contribution_record.md", "w") as fh:
        fh.write("")
print("Created file: docs\\contribution_record.md")

print("\n--- Setup Complete ---")