# Brute-Force Closest Pair Pseudocode

```text
CLOSEST-PAIR(points)
  require at least two points
  best_squared = infinity; pairs = 0
  for i = 0 to n - 2
    for j = i + 1 to n - 1
      dx = points[i].x - points[j].x
      dy = points[i].y - points[j].y
      squared = dx*dx + dy*dy
      pairs += 1
      if squared < best_squared
        best_squared = squared; best_pair = (points[i], points[j])
  return best_pair, sqrt(best_squared), pairs
```

The `j > i` loop examines each unordered pair once, hence $1+2+...+(n-1)=n(n-1)/2$ pairs. A strict improvement retains the first pair in input order on ties; duplicate coordinates therefore produce distance zero.