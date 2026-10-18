# Task 6 — Formulate the recurrence

The recurrence is for the recursive binary-search procedure, not the separate
sorting phase. Let `n` be the number of candidates in the current sorted
interval.

- Original input size: `n` candidate registration numbers.
- Recursive subproblem: at most `floor(n/2)` candidates remain after comparing
  the middle key.
- Number of recursive calls: one call on only one half (not two calls).
- Non-recursive work: one middle-index calculation and a constant number of
  key comparisons and branch operations, denoted `c`.
- Base case: an empty interval (`n = 0`) returns not-found in constant time,
  denoted `T(0) = d`.

Thus, for `n > 0`, a size-sensitive form is

`T(n) = T(floor(n/2)) + c`, with `T(0) = d`.

Using `ceil(n/2)` instead changes only rounding, not the asymptotic result.
The recurrence follows the algorithm's single recursive call and the halving
step; it is not a recurrence for merge sort or a two-branch recursion.
