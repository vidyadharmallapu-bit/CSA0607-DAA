# Task 3 — Derive the time-complexity functions

Let `n` be the number of unique records and `q` the number of searches. Assume
the initial collection is unsorted unless a structure is explicitly prepared.
Use a unit-cost model for a key comparison/hash lookup; actual string lengths
and machine constants affect measured time but not these growth classes.

## Linear search

If the record is at zero-based position `j`, the scan executes `j + 1`
equality tests. A missing key executes `n` tests. Under uniformly likely
successful positions, the mean is

`(1 + 2 + ... + n) / n = n(n + 1) / (2n) = (n + 1) / 2`.

Thus a successful average search has
`T_L(n) = a + b(n + 1)/2`; an unsuccessful or worst-case search has
`T_L(n) = a + bn`. There is no preparation cost, so `q` arbitrary searches
cost `Theta(qn)` in the worst case (and approximately `q(n+1)/2` comparisons
for uniformly placed successful keys).

## Recursive binary search

For an unsorted input, comparison sorting costs `S(n) = Theta(n log n)`.
One search makes at most about `ceil(log2(n + 1))` middle-element probes:
each unsuccessful comparison reduces the remaining candidate interval from
`m` to at most `floor(m/2)`. Hence `B(n) = Theta(log n)` in the average and
worst cases, with a one-comparison best case.

Including preprocessing, `q` searches cost
`T_B(n,q) = S(n) + q B(n) = Theta(n log n + q log n)`.
If the records arrive sorted and remain sorted, the sorting term can be
omitted; that is a different input/update assumption.

## Hash-index lookup

Building a map by inserting each of `n` records takes expected
`H_build(n) = Theta(n)` time and `Theta(n)` extra space. With a suitable
hash distribution and bounded load factor, a lookup takes expected
`H_search(n) = Theta(1)` time. Therefore
`T_H(n,q) = Theta(n + q)` expected for a build followed by `q` lookups.
If all keys collide, one lookup can take `Theta(n)` and `q` lookups can take
`Theta(qn)`; this is the theoretical worst case, not the expected operating
case for a normal dictionary.

For `n = 1,000,000`, one linear miss needs one million equality tests; a
binary lookup needs about 20 levels; a hash lookup is expected to inspect a
constant number of entries after the one-time linear index build. These
counts explain why construction and query volume must be considered together.
