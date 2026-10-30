# Complexity Analysis

Let n be alert, blocklist, text, or event count, as appropriate; let m be pattern length and h the number of repeated lookups.

| Function/version | Basic operations | Best | Average | Worst | Auxiliary space |
|---|---|---:|---:|---:|---:|
| Original insertion sort | Severity comparisons and array writes | O(n) comparisons | O(n^2) | O(n^2) | O(1) |
| Corrected insertion sort | Same operations; preserves stable order | O(n) | O(n^2) | O(n^2) | O(1) |
| Optimized insertion sort | Counted comparisons and shifts | O(n) | O(n^2) | O(n^2) | O(1) |
| Stable merge-sort alternative | Merge comparisons and writes | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Original/corrected sequential search | Key comparisons | O(1) hit first | O(n) | O(n) miss/last hit | O(1) |
| Hash-index construction | Insert blocklist addresses into set | O(n) expected | O(n) expected | O(n^2) pathological | O(n) |
| Hash lookup, each / h queries | Membership probes | O(1) expected | O(1) expected | O(n) pathological per query | O(n) index |
| Original/corrected brute matcher | Character comparisons | O(m) early match | input-dependent | O((n-m+1)m) | O(output matches) |
| Optimized counted brute matcher | Character comparisons with mismatch exit | O(m) | input-dependent | O((n-m+1)m) | O(output matches) |
| Original/corrected closest-pair brute force | Unique pair distance calculations | Θ(n²) | Θ(n²) | Θ(n²) | O(1) beyond input |
| Optimized exact divide-and-conquer | Sort, partition, merge, bounded strip distances | O(n log n) | O(n log n) | O(n log n) | O(n) |

The original broken routines may appear to do less work because they terminate early or omit valid alignments; their apparent speed is not an optimization. Insertion sort is attractive for small nearly sorted batches but has quadratic shifts for random/reverse input. The merge alternative pays buffer allocation and extra writes for a predictable O(n log n) bound.

Set lookup is expected constant time under ordinary hash behavior, not a deterministic worst-case guarantee. Index construction and memory must be included when comparing a small number of lookups. Instrumentation increments counters and affects timing; operation counts and timings are therefore reported separately.

Squared distances preserve ordering among nonnegative Euclidean distances and avoid a square root for each brute-force pair, but do not change the baseline's Θ(n²) pair count. The optimized closest-pair method establishes a valid within-half upper bound before strip pruning, retains equal-distance strip candidates for deterministic tie-breaking, and checks at most seven following points by the 2-D packing argument. Duplicate coordinates are detected first and return the lexicographically earliest zero-distance pair. Sorting and y-partitioning cost O(n log n) time and O(n) auxiliary memory. All coordinate fixtures use finite real-valued kilometres.
