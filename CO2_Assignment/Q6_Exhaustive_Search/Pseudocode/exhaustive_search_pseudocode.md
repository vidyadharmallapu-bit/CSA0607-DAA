# Exhaustive Knapsack Search Pseudocode

```text
EXHAUSTIVE-KNAPSACK(packages, capacity)
  best = empty subset with value 0 and weight 0
  for mask = 0 to 2^n - 1
    weight = value = 0; selected = empty list
    for i = 0 to n - 1
      if bit i of mask is set
        add package i's weight and value; record its ID
    if weight <= capacity
      feasible += 1
      if candidate improves value, then lower weight, then lexical ID tie-break
        save candidate as best
  return best, 2^n subsets examined, feasible
```

Positive weights and nonnegative values are required. The empty mask guarantees a feasible baseline whenever capacity is nonnegative.