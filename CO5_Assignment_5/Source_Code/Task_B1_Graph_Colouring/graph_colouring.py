"""
Task B1 – Graph Colouring with Backtracking (Instrumented)
CSA06 Design and Analysis of Algorithms – CO5 Assignment 5
Student: MALLAPU VIDYADHAR

Implements:
  - Backtracking graph colouring with full instrumentation
  - Version 1: Input-order vertex selection
  - Version 2: Most-Constrained-Vertex (MCV) heuristic ordering
"""

import time
from typing import List, Dict, Optional, Tuple


# ─────────────────────────────────────────────
# Graph representation
# ─────────────────────────────────────────────
class Graph:
    def __init__(self, num_vertices: int):
        self.V = num_vertices
        self.adj = [[] for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int):
        self.adj[u].append(v)
        self.adj[v].append(u)

    def degree(self, v: int) -> int:
        return len(self.adj[v])


# ─────────────────────────────────────────────
# Search Instrumentation counters
# ─────────────────────────────────────────────
class Stats:
    def __init__(self):
        self.nodes_visited      = 0
        self.candidates_tried   = 0
        self.branches_rejected  = 0
        self.backtracks         = 0
        self.max_depth          = 0

    def reset(self):
        self.__init__()

    def report(self):
        print(f"  Search nodes visited      : {self.nodes_visited}")
        print(f"  Candidate assignments tried: {self.candidates_tried}")
        print(f"  Branches rejected (pruned) : {self.branches_rejected}")
        print(f"  Backtracks                 : {self.backtracks}")
        print(f"  Maximum search depth       : {self.max_depth}")


# ─────────────────────────────────────────────
# Core feasibility check
# ─────────────────────────────────────────────
def is_safe(graph: Graph, colour: List[int], vertex: int, c: int) -> bool:
    """Return True if assigning colour c to vertex does not conflict."""
    for neighbour in graph.adj[vertex]:
        if colour[neighbour] == c:
            return False
    return True


# ─────────────────────────────────────────────
# VERSION 1 – Input-order vertex selection
# ─────────────────────────────────────────────
def _backtrack_v1(graph: Graph, num_colours: int, colour: List[int],
                  vertex: int, stats: Stats) -> bool:
    stats.nodes_visited += 1
    stats.max_depth = max(stats.max_depth, vertex)

    # Goal condition: all vertices assigned
    if vertex == graph.V:
        return True

    for c in range(1, num_colours + 1):
        stats.candidates_tried += 1
        if is_safe(graph, colour, vertex, c):
            colour[vertex] = c                              # Assign
            if _backtrack_v1(graph, num_colours, colour, vertex + 1, stats):
                return True
            colour[vertex] = 0                              # Undo (backtrack)
            stats.backtracks += 1
        else:
            stats.branches_rejected += 1

    return False


def graph_colour_v1(graph: Graph, num_colours: int) -> Tuple[Optional[List[int]], Stats]:
    colour = [0] * graph.V
    stats  = Stats()
    found  = _backtrack_v1(graph, num_colours, colour, 0, stats)
    return (colour if found else None, stats)


# ─────────────────────────────────────────────
# VERSION 2 – Most-Constrained-Vertex heuristic
# Selection rule: choose the uncoloured vertex with
#   the highest number of ALREADY-COLOURED neighbours
#   (ties broken by overall degree – highest first).
# Rationale: colouring the most-constrained vertex first
#   exposes conflicts early and prunes more branches.
# ─────────────────────────────────────────────
def _most_constrained_vertex(graph: Graph, colour: List[int], uncoloured: List[int]) -> int:
    def priority(v):
        coloured_nbrs = sum(1 for nb in graph.adj[v] if colour[nb] != 0)
        return (coloured_nbrs, graph.degree(v))   # maximise both

    return max(uncoloured, key=priority)


def _backtrack_v2(graph: Graph, num_colours: int, colour: List[int],
                  uncoloured: List[int], depth: int, stats: Stats) -> bool:
    stats.nodes_visited += 1
    stats.max_depth = max(stats.max_depth, depth)

    if not uncoloured:
        return True

    # Pick the most-constrained vertex
    vertex = _most_constrained_vertex(graph, colour, uncoloured)
    remaining = [v for v in uncoloured if v != vertex]

    for c in range(1, num_colours + 1):
        stats.candidates_tried += 1
        if is_safe(graph, colour, vertex, c):
            colour[vertex] = c
            if _backtrack_v2(graph, num_colours, colour, remaining, depth + 1, stats):
                return True
            colour[vertex] = 0
            stats.backtracks += 1
        else:
            stats.branches_rejected += 1

    return False


def graph_colour_v2(graph: Graph, num_colours: int) -> Tuple[Optional[List[int]], Stats]:
    colour    = [0] * graph.V
    stats     = Stats()
    uncoloured = list(range(graph.V))
    found     = _backtrack_v2(graph, num_colours, colour, uncoloured, 0, stats)
    return (colour if found else None, stats)


# ─────────────────────────────────────────────
# Pretty printer
# ─────────────────────────────────────────────
def print_colouring(colour: Optional[List[int]]):
    if colour is None:
        print("  No valid colouring found.")
    else:
        for v, c in enumerate(colour):
            print(f"    Vertex {v} → Colour {c}")


def run_test(title: str, graph: Graph, k: int, purpose: str):
    sep = "─" * 60
    print(f"\n{sep}")
    print(f"TEST: {title}")
    print(f"Purpose: {purpose}")
    print(f"Vertices: {graph.V}  |  k = {k} colours")
    print(sep)

    print("\n[Version 1 – Input Order]")
    t0 = time.perf_counter()
    col1, s1 = graph_colour_v1(graph, k)
    t1 = time.perf_counter()
    print_colouring(col1)
    s1.report()
    print(f"  Time: {(t1-t0)*1000:.3f} ms")

    print("\n[Version 2 – Most-Constrained-Vertex Heuristic]")
    t0 = time.perf_counter()
    col2, s2 = graph_colour_v2(graph, k)
    t1 = time.perf_counter()
    print_colouring(col2)
    s2.report()
    print(f"  Time: {(t1-t0)*1000:.3f} ms")

    print("\n[Comparison Table]")
    print(f"  {'Measure':<30} {'V1':>8} {'V2':>8}")
    print(f"  {'─'*46}")
    for label, v1, v2 in [
        ("Search nodes visited",    s1.nodes_visited,     s2.nodes_visited),
        ("Candidate assignments",   s1.candidates_tried,  s2.candidates_tried),
        ("Branches rejected",       s1.branches_rejected, s2.branches_rejected),
        ("Backtracks",              s1.backtracks,        s2.backtracks),
        ("Max depth",               s1.max_depth,         s2.max_depth),
    ]:
        print(f"  {label:<30} {v1:>8} {v2:>8}")


# ─────────────────────────────────────────────
# Test suite – B1.1 Test cases
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print(" TASK B1 – GRAPH COLOURING WITH BACKTRACKING")
    print("=" * 60)

    # ── TEST 1: Colourable graph (cycle C5, k=3) ──────────────────
    g1 = Graph(5)
    for u, v in [(0,1),(1,2),(2,3),(3,4),(4,0)]:
        g1.add_edge(u, v)
    run_test(
        "TEST 1 – Colourable: 5-cycle C5, k=3",
        g1, k=3,
        purpose="Verify algorithm finds a valid 3-colouring for a colourable graph."
    )

    # ── TEST 2: Not colourable (K4 complete graph, k=3) ──────────
    g2 = Graph(4)
    for u, v in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]:
        g2.add_edge(u, v)
    run_test(
        "TEST 2 – Not Colourable: K4 complete graph, k=3",
        g2, k=3,
        purpose="Verify algorithm correctly reports no solution when k < chromatic number."
    )

    # ── TEST 3: Boundary case – single vertex, k=1 ───────────────
    g3 = Graph(1)
    run_test(
        "TEST 3 – Boundary: 1 vertex, k=1",
        g3, k=1,
        purpose="Boundary condition: a single isolated vertex is trivially 1-colourable."
    )

    # ── TEST 4: Larger graph (Petersen graph, k=3) ───────────────
    g4 = Graph(10)
    for u, v in [(0,1),(1,2),(2,3),(3,4),(4,0),         # outer 5-cycle
                 (5,7),(7,9),(9,6),(6,8),(8,5),          # inner pentagram
                 (0,5),(1,6),(2,7),(3,8),(4,9)]:         # spokes
        g4.add_edge(u, v)
    run_test(
        "TEST 4 – Petersen Graph (10 vertices), k=3",
        g4, k=3,
        purpose="Verify on a well-known graph. Petersen graph has chromatic number 3."
    )

    # ── TEST 5: Bipartite graph (easily 2-colourable) ─────────────
    g5 = Graph(6)
    for u, v in [(0,3),(0,4),(0,5),(1,3),(1,4),(2,5)]:
        g5.add_edge(u, v)
    run_test(
        "TEST 5 – Bipartite K3,3 variant, k=2",
        g5, k=2,
        purpose="Bipartite graphs are always 2-colourable; test ordering heuristic."
    )

    print("\n" + "=" * 60)
    print("B1.2 – Design vs Implementation Note:")
    print("  Pseudocode closely matches implementation.")
    print("  Modification: Version 2 passes 'uncoloured' list rather")
    print("  than a vertex index, enabling dynamic MCV selection.")
    print("=" * 60)


if __name__ == "__main__":
    main()
