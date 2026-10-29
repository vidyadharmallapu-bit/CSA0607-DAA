# Sequential Search Pseudocode

```text
SEQUENTIAL-SEARCH(records, target)
  comparisons = 0
  for index = 0 to length(records) - 1
    comparisons += 1
    if records[index].tool_id = target
      return (index, comparisons)
  return (NOT-FOUND, comparisons)
```

The first matching record is returned. A miss compares the target with every record.