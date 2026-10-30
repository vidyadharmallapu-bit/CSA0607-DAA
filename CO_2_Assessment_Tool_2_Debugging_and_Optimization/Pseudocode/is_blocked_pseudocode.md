# Sequential Blocklist Search

```text
IS-BLOCKED(blocklist, ip)
  for each entry in blocklist from first to last
    if entry = ip
      return true
  return false
```

A hit stops immediately; a miss returns false only after the full scan. Time is O(1) best and O(n) average/worst; auxiliary space is O(1).
