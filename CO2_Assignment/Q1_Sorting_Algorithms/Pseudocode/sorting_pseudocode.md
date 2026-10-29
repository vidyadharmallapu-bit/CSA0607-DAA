# Sorting Algorithms Pseudocode

All three procedures sort the input array in place. A comparison is one key comparison. A swap counts as three element movements (two stores and one temporary-value save); insertion sort counts each shift and final key write as one movement.

## Selection Sort

```text
SELECTION-SORT(A)
  for start = 0 to length(A) - 2
    minimum = start
    for i = start + 1 to length(A) - 1
      comparisons = comparisons + 1
      if A[i] < A[minimum]
        minimum = i
    if minimum != start
      swap A[start], A[minimum]
      swaps = swaps + 1; movements = movements + 3
```

## Bubble Sort with Early Exit

```text
BUBBLE-SORT(A)
  for end = length(A) - 1 down to 1
    changed = false
    for i = 0 to end - 1
      comparisons = comparisons + 1
      if A[i] > A[i + 1]
        swap adjacent values; swaps = swaps + 1; movements += 3
        changed = true
    if not changed
      stop
```

## Insertion Sort

```text
INSERTION-SORT(A)
  for i = 1 to length(A) - 1
    key = A[i]; j = i - 1
    while j >= 0
      comparisons += 1
      if A[j] <= key
        break
      A[j + 1] = A[j]; movements += 1; j -= 1
    A[j + 1] = key; movements += 1
```