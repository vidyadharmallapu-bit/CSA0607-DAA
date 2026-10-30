# Stable Alert Sort (Descending Severity)

```text
SORT-ALERTS(alerts)
  for i = 1 to length(alerts) - 1
    key = alerts[i]
    j = i - 1
    while j >= 0 and alerts[j].severity < key.severity
      alerts[j + 1] = alerts[j]
      j = j - 1
    alerts[j + 1] = key
  return alerts
```

The input list is mutated. The strict `<` shift condition leaves equal-severity arrivals in their original order. Best case is O(n); average and worst cases are O(n^2); auxiliary space is O(1).
