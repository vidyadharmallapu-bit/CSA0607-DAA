# Brute-Force String Matching Pseudocode

```text
BRUTE-FORCE-MATCH(text, pattern)
  if pattern is empty
    return every boundary 0..length(text), 0 comparisons
  if length(pattern) > length(text)
    return no matches, 0 comparisons
  matches = []; comparisons = 0
  for start = 0 to length(text) - length(pattern)
    offset = 0
    while offset < length(pattern)
      comparisons += 1
      if text[start + offset] != pattern[offset]
        break
      offset += 1
    if offset = length(pattern)
      append start to matches
  return matches, comparisons
```

Match offsets are zero-based. Advancing `start` by one preserves overlapping occurrences.