# Task 10 — Compare theory with experiment

Use the measured values in Task 9's CSV rather than treating asymptotic
notation as a timing prediction. The experiment holds the query mix constant
and measures the three actual implementations at four increasing input sizes.
Expected behavior is that linear scan time increases with `n`, recursive
binary-search time grows slowly with search depth after sorting, and hash
lookup remains approximately flat while index construction grows with `n`.

The measured data and graph should be inspected together: timings at small
sizes can be dominated by Python call overhead, timer resolution, allocation,
and cache effects. Big-O omits constants, string hashing/comparison costs,
memory allocation, cache behavior, and operating-system scheduling. Binary
search's sort time is a one-time cost, not part of each subsequent lookup;
the hash build time likewise belongs in the total only when creating or
rebuilding the index.

For the changed one-million-record workload, use the measured per-query
values in the CSV to estimate 50,000 searches, and add that size's measured
preprocessing time once. These are projections from the sampled benchmark,
not a measured run of 50,000 timed requests. The reproduction script and
actual environment are documented in Task 8.

In this run, increasing the dataset by a factor of 1,000 (1,000 to 1,000,000)
raised linear scan time from about 18.73 us to 245,511.11 us per query. The
recursive search rose from about 1.77 us to 11.66 us, while hash lookup was
about 0.087 us and 0.227 us at those endpoints. The measured build costs at
one million were 0.645 s for sorting and 0.438 s for the dictionary. The
slight non-monotonic values in intermediate rows show why asymptotic
complexity predicts trends rather than exact timing. The large linear scan
increase and small query costs after preprocessing are consistent with the
theoretical growth; build costs remain visible and must be included when an
index is created.
