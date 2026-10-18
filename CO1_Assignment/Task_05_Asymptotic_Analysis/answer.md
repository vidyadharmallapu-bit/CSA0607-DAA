# Task 5 — Asymptotic analysis

| Approach | Search-only bound | Preparation and space | Growth interpretation |
|---|---|---|---|
| Linear scan | Best `Theta(1)`; average/worst `Theta(n)` | No preprocessing; `Theta(1)` auxiliary space | Doubling records roughly doubles the average scan work. |
| Recursive binary search | Best `Theta(1)`; average/worst `Theta(log n)` | Sorting `Theta(n log n)` once; sorted copy `Theta(n)` space. Recursive stack `Theta(log n)`. | Doubling records adds about one probe per search, after sorting. |
| Hash index | Expected `Theta(1)`; worst `Theta(n)` | Expected build `Theta(n)`; index `Theta(n)` space | Expected lookup work remains nearly flat as the number of keys grows, provided hashing and load factor remain suitable. |

`O` describes an asymptotic upper bound, `Omega` a lower bound, and `Theta`
a tight bound when both apply. For a successful linear search at a fixed
position, the exact count is `j+1`; uniformly averaged successful searches
are `Theta(n)`. Binary search is `Omega(1)` for a midpoint hit and
`Theta(log n)` for average/worst search depth. Hash lookup is expected
`Theta(1)` but worst-case `Theta(n)` under collisions.

For one million records, average linear scanning examines about 500,000
entries for a successful uniformly placed target (one million for a miss),
binary search needs about 20 probes, and a hash index expects constant
lookup work. The input growth from 1,000 to 1,000,000 therefore changes
the work from hundreds to hundreds of thousands of linear comparisons, from
roughly ten to twenty binary levels, and little expected per-request hash
work, while the hash's storage and build costs still grow linearly.
