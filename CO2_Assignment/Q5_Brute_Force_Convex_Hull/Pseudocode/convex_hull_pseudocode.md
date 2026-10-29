# Brute-Force Convex Hull Pseudocode

```text
BRUTE-HULL(points)
  remove duplicate coordinates
  handle 0, 1, and 2 unique points directly
  boundary_extremes = empty set
  for every unordered pair (A, B)
    evaluate cross(A, B, P) for every other P
    if nonzero signs occur on both sides
      continue: line is not supporting
    collect all points collinear with A-B
    add the two extreme collinear points to boundary_extremes
  if all points are collinear
    return the two lexicographic extremes
  order unique boundary extremes by polar angle around their centroid
  return ordered extremes
```

`cross(A,B,P)=(Bx-Ax)(Py-Ay)-(By-Ay)(Px-Ax)`. Positive and negative values mean opposite sides of the directed line; zero means collinear. A supporting line has no points on both strict sides. Keeping only the segment extremes prevents intermediate collinear points from becoming polygon corners.