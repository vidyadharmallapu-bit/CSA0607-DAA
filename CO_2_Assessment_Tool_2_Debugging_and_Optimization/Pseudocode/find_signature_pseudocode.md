# Brute-Force Signature Matching

```text
FIND-SIGNATURE(text, pattern)
  if pattern is empty
    return boundaries 0 through length(text)
  if length(pattern) > length(text)
    return empty list
  hits = empty list
  for start = 0 to length(text) - length(pattern)
    offset = 0
    while offset < length(pattern) and text[start + offset] = pattern[offset]
      offset = offset + 1
    if offset = length(pattern)
      append start to hits
  return hits
```

All positions are zero-based. Advancing one alignment at a time reports overlaps. The empty pattern is defined to match all n+1 boundaries. Worst-case comparisons are O((n-m+1)m), or O(nm) when n >= m.
