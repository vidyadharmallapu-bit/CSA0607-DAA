# Branch-and-Bound Knapsack Pseudocode

```text
BRANCH-AND-BOUND(items, capacity)
  sort by descending value/weight ratio
  best = empty subset
  SEARCH(index=0, weight=0, value=0, chosen=empty)

SEARCH(index, weight, value, chosen)
  visited += 1
  if weight > capacity
    pruned += 1; return
  if fractional_relaxation_upper_bound(index, weight, value) < best.value
    pruned += 1; return
  if index = n
    compare feasible leaf with best using the documented tie-break; return
  expanded += 1
  SEARCH(index+1, weight+items[index].weight,
         value+items[index].value, chosen plus item)
  SEARCH(index+1, weight, value, chosen)
```

The relaxation takes whole remaining items while they fit, then a fraction of the next item. It is an upper bound because it relaxes the 0/1 restriction. Pruning uses strict `<` so equal-value branches remain available to satisfy the lower-weight/lexical tie-break.