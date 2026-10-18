# Task 2 — Identify the basic operation

| Approach | Dominant operation | Location and reason |
|---|---|---|
| Iterative linear search | Equality test between the current registration number and the target | Executed once per inspected record. The scan ends at a hit or after all `n` records, so the count grows linearly with the search position. |
| Recursive binary search | Key comparison at the middle element (equality and, if unequal, ordering) | Executed once per recursive level. Each comparison discards about half the remaining range, so the count grows with the number of halvings. |
| Hash-index lookup | Hash computation and key equality in the selected bucket/probe sequence | Performed by the map lookup after building the index. With a well-distributed hash and controlled load factor, only a constant expected number of keys are examined; collisions can increase this to `n`. |

These operations are suitable because each drives how much input-dependent
work is done by a search. Hash operations also include hashing the target key;
they are not literally equivalent to one list equality comparison. Index
construction is a separate cost and is analysed in Task 3.
