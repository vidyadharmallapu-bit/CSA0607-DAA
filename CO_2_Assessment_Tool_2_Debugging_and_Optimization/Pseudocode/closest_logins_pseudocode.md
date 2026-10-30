# Closest Login Events

## Correct brute-force baseline

```text
CLOSEST-LOGINS(events)
  require at least two events
  bestSquared = infinity
  for i = 0 to n - 2
    for j = i + 1 to n - 1
      squared = squaredDistance(events[i], events[j])
      if squared < bestSquared, or equal with lexicographically smaller (i,j)
        save squared and pair (i,j)
  return pair, squareRoot(bestSquared)
```

This visits exactly n(n-1)/2 unique pairs and uses O(n^2) time, O(1) auxiliary space.

## Exact divide-and-conquer optimization

```text
CLOSEST-PAIR(xSorted, ySorted)
  if at most 3 points: compare all pairs and return y-sorted points
  split xSorted into left and right halves
  partition ySorted by original point identity
  solve each half; keep the better distance and index-pair tie-break
  merge both y-orders
  collect points whose squared x-offset from split <= bestSquared
  in y-order, compare each point with at most the next 7 strip points
    stop when squared y-offset > bestSquared
    update best distance and lexicographic index-pair tie-break
  return best result and merged y-order
```

Duplicate coordinates are grouped before recursion: any duplicate gives the global minimum 0, and the lexicographically earliest duplicate pair is returned. Otherwise all distances are positive. The standard two-dimensional packing argument bounds strip comparisons to seven following points after each split; the strip test cannot discard a pair closer than the current bound. Runtime is O(n log n), auxiliary memory O(n), including sorting and recursion data.
