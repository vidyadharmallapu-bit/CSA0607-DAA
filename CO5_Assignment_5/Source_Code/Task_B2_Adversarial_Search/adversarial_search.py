"""
Task B2 – Adversarial Search: Same Size, Very Different Search
CSA06 Design and Analysis of Algorithms – CO5 Assignment 5
Student: MALLAPU VIDYADHAR

Uses the Graph Colouring backtracking solver from Task B1.
Constructs two graphs of the same size (V=7, k=3) with
contrasting search behaviour:

  Graph A – Easy (sparse / structured)  → little backtracking
  Graph B – Hard (dense / adversarial)  → heavy backtracking
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Task_B1_Graph_Colouring'))

from graph_colouring import Graph, graph_colour_v1, Stats
import time


# ─────────────────────────────────────────────
# Graph A – Easy instance (path graph + small cycle)
# A path is 2-colourable; adding one more colour makes it trivial.
# No clique larger than 2 → pruning happens very rarely.
# ─────────────────────────────────────────────
def build_graph_A() -> Graph:
    """
    7-vertex path: 0-1-2-3-4-5-6
    Prediction: very few backtracks because vertices are assigned
    left-to-right; each next vertex has at most 1 coloured neighbour.
    """
    g = Graph(7)
    for u, v in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6)]:
        g.add_edge(u, v)
    return g


# ─────────────────────────────────────────────
# Graph B – Hard instance (dense, near-complete)
# A graph close to K7 forces many backtracks with k=3.
# Every vertex sees many coloured neighbours → conflicts
# arise immediately → extensive pruning AND backtracks.
# ─────────────────────────────────────────────
def build_graph_B() -> Graph:
    """
    7-vertex graph: 3 disjoint triangles sharing one vertex (0).
    Triangle 1: 0-1-2-0
    Triangle 2: 0-3-4-0
    Triangle 3: 0-5-6-0
    Plus cross-edges: 1-3, 2-4, 5-3
    This creates a dense conflict structure.
    With k=3 the colouring is tight; vertex 0 is the most constrained.
    """
    g = Graph(7)
    for u, v in [
        (0,1),(1,2),(2,0),   # triangle 1
        (0,3),(3,4),(4,0),   # triangle 2
        (0,5),(5,6),(6,0),   # triangle 3
        (1,3),(2,4),(5,3),   # cross-edges creating extra conflicts
    ]:
        g.add_edge(u, v)
    return g


# ─────────────────────────────────────────────
# Runner
# ─────────────────────────────────────────────
def run_adversarial(label: str, graph: Graph, k: int, prediction: str):
    print(f"\n{'='*60}")
    print(f"  {label}  |  V={graph.V}  |  k={k}")
    print(f"{'='*60}")
    print(f"Prediction: {prediction}")

    t0 = time.perf_counter()
    colour, stats = graph_colour_v1(graph, k)
    t1 = time.perf_counter()

    if colour:
        print(f"\nSolution found: {colour}")
    else:
        print("\nNo valid colouring found with k colours.")

    print(f"\nSearch Statistics:")
    stats.report()
    print(f"  Time: {(t1-t0)*1000:.4f} ms")
    return stats


def main():
    K = 3

    print("=" * 60)
    print(" TASK B2 – ADVERSARIAL SEARCH ANALYSIS")
    print(" Graph A (Easy)  vs  Graph B (Hard)")
    print(f" Both: V=7, k={K}")
    print("=" * 60)

    # ── Predictions (stated before running) ──────────────────────
    pred_A = (
        "Path graph → at most 1 coloured neighbour at each step. "
        "Pruning happens rarely. Very few backtracks expected (< 5). "
        "Max depth = 7."
    )
    pred_B = (
        "Dense graph with triangles sharing vertex 0. Vertex 0 is "
        "constrained by 6 neighbours across 3 triangles. Expect many "
        "rejected branches and backtracks (> 20)."
    )

    gA = build_graph_A()
    gB = build_graph_B()

    sA = run_adversarial("Graph A – Easy (Path Graph 0-1-2-3-4-5-6)", gA, K, pred_A)
    sB = run_adversarial("Graph B – Hard (Dense Triangulated Graph)", gB, K, pred_B)

    # ── Comparison ───────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print("COMPARISON TABLE")
    print(f"  {'Measure':<28} {'Graph A':>8} {'Graph B':>8}")
    print(f"  {'─'*44}")
    for label, a, b in [
        ("Search nodes visited",   sA.nodes_visited,     sB.nodes_visited),
        ("Candidate assignments",  sA.candidates_tried,  sB.candidates_tried),
        ("Branches rejected",      sA.branches_rejected, sB.branches_rejected),
        ("Backtracks",             sA.backtracks,        sB.backtracks),
        ("Max depth",              sA.max_depth,         sB.max_depth),
    ]:
        flag = "  <<< MORE" if b > a else ""
        print(f"  {label:<28} {a:>8} {b:>8}{flag}")

    print(f"\n{'─'*60}")
    print("INVESTIGATION – Why input size alone does not describe effort:")
    print("""
  Both graphs have exactly 7 vertices and use k=3 colours, yet
  their search behaviour differs dramatically.

  Graph A (path): each vertex has at most 2 neighbours; the feasibility
  test rarely fails and backtracking is minimal.

  Graph B (dense): vertex 0 is adjacent to ALL other vertices. Its
  3 triangles force colour conflicts immediately; the solver must try
  multiple colour assignments, reject them, and backtrack repeatedly.

  Structural property causing extra search:
    → HIGH LOCAL CLIQUE DENSITY: the shared vertex 0 belongs to
      three overlapping triangles, creating a chromatic constraint
      that cannot be satisfied greedily. The algorithm must exhaust
      colour assignments at this bottleneck vertex before finding a
      valid assignment, or reporting failure.

  Conclusion: computational effort is determined by CONSTRAINT DENSITY
  (edge density, clique sizes, degree distribution), NOT by |V| alone.
""")


if __name__ == "__main__":
    main()
