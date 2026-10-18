# Task 12 — Re-evaluate and adapt the design

## A. Impact analysis

The scale is now specified: one million records and 50,000 requests each hour,
with new records arriving only once per day. Search volume is no longer an
unspecified occasional operation; it is a sustained high-frequency path.
The earlier assumption that preprocessing might be expensive relative to a
small number of searches is weakened. Conversely, the low update frequency
makes it practical to build and maintain an auxiliary search index without
paying an update cost for every lookup. The relevant comparison is
preprocessing plus 1.2 million daily lookups, not search complexity alone.

## B. Evaluate the original recommendation

The hash index remains suitable. Its expected build is `Theta(n)` and expected
lookup is `Theta(1)`. The recurring cost for 50,000 requests/hour is expected
to be proportional to the number of requests, rather than to `n` per request.
The single build/rebuild cost is amortized across 1.2 million daily requests.
At one million records, a linear scan would average roughly 500,000 key
comparisons for a successful uniform hit (and one million for a miss), or
about 37.5 billion comparisons per hour for the benchmark's 50/50 hit/miss mix.
Binary search would take about 20 levels per lookup, but needs a sorted
structure and a `Theta(n log n)` initial sort if the source data is unsorted.
The locally measured one-million-row timings and build costs in Task 9 are
the empirical evidence; projections are not represented as a separately
measured 50,000-request batch.

## C. Adaptation or redesign

**Decision: retain the hash strategy and modify the operational design** to
maintain a registration-number index over the record store. On the daily
ingestion, validate uniqueness and either apply the new identifiers to the
index or build a replacement index and atomically publish it. For readers,
the replacement approach avoids observing a partially rebuilt index but
requires temporary memory for both versions. Incremental insertion is
expected amortized `O(1)` per new key, with occasional resizing; rebuilding
from the complete collection is expected `Theta(n)` time and `Theta(n)` space.
Each lookup remains expected `Theta(1)`, worst-case `Theta(n)` under severe
collisions.

## D. Evidence-based defence

The mathematical result is expected `Theta(n + q)` for index construction
and `q` lookups, versus `Theta(qn)` for repeated scans and
`Theta(n log n + q log n)` for sorting plus binary searches. With `q =
1,200,000` searches each day at the specified rate, the hash's one-time
linear build is amortized across a large number of expected constant-time
lookups. It consumes linear additional memory; the design is therefore
conditional on available capacity and correct index consistency.

Task 9's actual benchmark supplies the measured construction and lookup
times for the one-million-record dataset. In interpreting them, add the
measured daily build cost once, and multiply measured lookup time by the
request volume only as an estimate; the benchmark does not simulate
concurrent production traffic, network/database I/O, or real records.
For this run, the corresponding serial projections for one hour's 50,000
requests are about 12,275.56 seconds for linear search, 1.23 seconds for
sorting plus binary search, and 0.45 seconds for hash build plus lookup.
They are estimates from the median of five 30-query rounds, not a timed
50,000-request service run.
These limits are why the hash index is recommended for this exact-key,
read-heavy scenario, while a sorted index may be retained as a complementary
structure if ordered queries are needed.
