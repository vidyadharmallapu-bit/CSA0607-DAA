# Task 7 — Solve the recurrence

For binary search, `T(n) = T(floor(n/2)) + c` and `T(0) = d`, where `c` and
`d` are constants. The Master Theorem applies to the asymptotically equivalent
form `T(n) = 1 T(n/2) + Theta(1)`: there is one subproblem (`a = 1`), its size
is reduced by a factor of two (`b = 2`), and outside work is
`f(n) = Theta(1)`.

Compute the comparison term:

`n^(log_b(a)) = n^(log_2(1)) = n^0 = 1`.

Therefore `f(n) = Theta(n^(log_b(a)))`; this is Master Theorem Case 2 (the
equal-growth case), yielding `T(n) = Theta(log n)`.

The same result follows by iteration: after `k` calls the remaining size is
about `n / 2^k`. Stop when it is at most one, so `n / 2^k <= 1`, or
`k >= log2(n)`. Each level performs constant work; there are logarithmically
many levels. The base case adds constant work, so total time is `Theta(log n)`.

As `n` grows, the recursive search gains only about one comparison for each
doubling of the dataset. Its recursion stack uses `Theta(log n)` space. This
solution concerns searching an already-sorted array; sorting an initially
unsorted database remains a separate `Theta(n log n)` preprocessing cost.
