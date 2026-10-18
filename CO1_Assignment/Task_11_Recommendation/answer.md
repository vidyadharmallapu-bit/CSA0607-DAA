# Task 11 — Recommend and defend the final design

For the stated exact-registration-number lookup workload, use a hash index
mapping each unique registration number to its student record. It is expected
`Theta(n)` to build, expected `Theta(1)` per lookup, and requires `Theta(n)`
additional space. The benchmark's one-million-record measurements in
Task 9 should be considered with the construction time and the task's actual
lookup volume; the evidence is generated locally and is not a fabricated
performance claim.

This design is preferable to repeated linear scans because a miss or average
hit examines a large fraction of a million records. It avoids binary search's
mandatory ordering step (`Theta(n log n)`) and provides direct expected
lookups. Binary search remains reasonable when records are already kept
sorted, memory is constrained, or ordered/range queries are also required.
Linear search remains reasonable for very small collections or a one-off
lookup where index construction would not be repaid.

The hash approach trades additional memory and a full initial build for
high-volume retrieval. With daily additions, an application may add the daily
batch to the index or build a replacement index and publish it atomically;
either approach must maintain unique-key consistency. The result is practical
as the database grows if memory capacity and hash behavior are monitored.
Hash lookup's theoretical worst case remains linear, so the recommendation is
based on expected behavior and measured evidence, not a claim of a worst-case
constant bound.

In the recorded local run, one-million-record per-query measurements were
245.51 ms for linear scan, 11.66 us for recursive binary search, and 0.227 us
for hash lookup. For 50,000 serial queries plus the measured build/sort, the
projected totals are 12,275.56 s, 1.23 s, and 0.45 s, respectively. This
supports the index recommendation for a high-volume exact-key workload.
These are projections on one machine; they do not prove production throughput
or account for full-record I/O, concurrency, or persistence.
