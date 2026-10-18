# Task 1 — Design the algorithms

## Problem and assumptions

The input contains `n` unique registration numbers; the operation is to find
one requested number and return it if present. Inputs may be unsorted. Search
correctness assumes registration numbers use a consistent representation and
that the recursive binary-search input is sorted. The three methods are
different strategies: sequential search, divide-and-conquer search, and
index-based hashing.

## 1. Iterative linear search

**Idea.** Inspect records in their current order and stop at the first match.
It requires no preprocessing and remains correct for an unsorted collection.

**Pseudocode**

```text
LINEAR-SEARCH(A, x)
    for each record r in A
        if r = x
            return r
    return NOT-FOUND
```

This is the baseline for an unsorted or very small collection. It is simple,
but a late hit or miss may inspect every record.

## 2. Recursive binary search

**Idea.** Sort the registration numbers once. Compare the target with the middle
number and recursively keep only the half in which the target could occur.

**Pseudocode**

```text
RECURSIVE-BINARY-SEARCH(A, x, low, high)
    if low > high
        return NOT-FOUND
    middle = floor((low + high) / 2)
    if A[middle] = x
        return A[middle]
    if x < A[middle]
        return RECURSIVE-BINARY-SEARCH(A, x, low, middle - 1)
    return RECURSIVE-BINARY-SEARCH(A, x, middle + 1, high)
```

Sorting is preprocessing; its cost must be counted when the original records
are not already sorted. This divide-and-conquer strategy provides predictable
logarithmic search and preserves sorted order for range queries and ordered
reports.

## 3. Hash-index lookup

**Idea.** Build a mapping from each unique registration number to its record
(or record location). Compute the key's hash and use the mapping to retrieve
the corresponding record.

**Pseudocode**

```text
BUILD-INDEX(A)
    H = empty hash map
    for each record r in A
        H[r.registration_number] = r
    return H

HASH-SEARCH(H, x)
    if x is a key in H
        return H[x]
    return NOT-FOUND
```

The index takes additional memory and construction time. It is selected because
the question concerns frequent exact-key retrieval and registration numbers
are unique. Hash lookup is expected constant time, but its worst case is linear
if many keys collide.
