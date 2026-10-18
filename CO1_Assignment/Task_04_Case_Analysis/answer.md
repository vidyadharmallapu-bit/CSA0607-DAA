# Task 4 — Best, average and worst cases

| Approach | Best case and work | Average case and work | Worst case and work |
|---|---|---|---|
| Linear search | Target is first: 1 equality test. | Successful target position is uniformly distributed: `(n+1)/2` tests on average. | Target is last or absent: `n` tests. No preprocessing. |
| Recursive binary search | Target equals the first middle element: 1 comparison. | For a uniformly distributed target in a balanced sorted array, the search follows a logarithmic-depth path: `Theta(log n)` comparisons. | Target is absent or lies at maximum depth: at most `ceil(log2(n+1))` probes, hence `Theta(log n)`. If unsorted initially, all cases also pay the one-time `Theta(n log n)` sorting cost. |
| Hash lookup | Target's bucket is immediately available with no collision: expected constant work. | Well-distributed keys and bounded load factor: expected `Theta(1)` work. | A long collision chain: `Theta(n)` key checks for one lookup. Index construction is expected `Theta(n)` and uses `Theta(n)` additional space. |

For linear search, the case is determined by where a successful target appears,
or whether it appears at all. Binary search halves the candidate interval on
every level, so even an absent key has logarithmic depth. Hash performance
depends on the distribution of hash values and the map's collision handling,
not on the target's original position. The average-case statements assume the
stated input distributions; they are not guarantees for every dataset.
