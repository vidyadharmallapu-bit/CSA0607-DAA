"""
Task B4 – Bin Packing Under a Production Constraint
CSA06 Design and Analysis of Algorithms – CO5 Assignment 5
Student: MALLAPU VIDYADHAR

Models cloud-infrastructure workload assignment:
  - Each workload has a resource demand 0 < d ≤ capacity C
  - Each server has identical capacity C
  - Objective: use as few servers as possible

Implements:
  First Fit Decreasing (FFD) heuristic
  + small exact solver (brute-force) for challenge comparison

B4.1 – Practical strategy: First Fit Decreasing (FFD)
  Rule: sort workloads largest-first; for each workload,
        place it in the first server with enough remaining capacity;
        open a new server if none fit.

Approximation guarantee:
  FFD ≤ (11/9)·OPT + 6/9  (de la Vega & Lueker, 1981)
"""

import time
import itertools
from typing import List, Dict, Tuple, Optional


# ─────────────────────────────────────────────
# First Fit Decreasing (FFD)
# ─────────────────────────────────────────────
def first_fit_decreasing(workloads: List[float], capacity: float
                         ) -> Tuple[List[List[float]], List[float]]:
    """
    Returns:
        bins     : list of servers, each containing assigned workloads
        remaining: remaining capacity per server
    """
    sorted_wl = sorted(workloads, reverse=True)
    bins: List[List[float]] = []
    remaining: List[float]  = []

    for w in sorted_wl:
        placed = False
        for i in range(len(bins)):
            if remaining[i] >= w:
                bins[i].append(w)
                remaining[i] -= w
                placed = True
                break
        if not placed:
            bins.append([w])
            remaining.append(capacity - w)

    return bins, remaining


# ─────────────────────────────────────────────
# Exact solver (brute-force, small instances only)
# ─────────────────────────────────────────────
def exact_bin_packing(workloads: List[float], capacity: float
                      ) -> Tuple[int, List[List[float]]]:
    """
    Finds the minimum number of bins via exhaustive search.
    Only practical for n ≤ 12 workloads.
    """
    n = len(workloads)

    for num_bins in range(1, n + 1):
        # Try every assignment of n workloads into num_bins bins
        for assignment in itertools.product(range(num_bins), repeat=n):
            bins_load = [0.0] * num_bins
            valid = True
            for i, b in enumerate(assignment):
                bins_load[b] += workloads[i]
                if bins_load[b] > capacity + 1e-9:
                    valid = False
                    break
            if valid:
                bins = [[] for _ in range(num_bins)]
                for i, b in enumerate(assignment):
                    bins[b].append(workloads[i])
                return num_bins, bins

    return n, [[w] for w in workloads]


# ─────────────────────────────────────────────
# Display helpers
# ─────────────────────────────────────────────
def print_allocation(bins: List[List[float]], remaining: List[float], capacity: float,
                     label: str = "FFD"):
    print(f"\n  [{label}] Servers used: {len(bins)}  |  Capacity: {capacity}")
    for i, (server, rem) in enumerate(zip(bins, remaining)):
        load = capacity - rem
        bar  = "█" * int(load / capacity * 20)
        print(f"    Server {i+1}: {server}  |  Load={load:.1f}/{capacity}  "
              f"Remaining={rem:.1f}  [{bar:<20}]")


# ─────────────────────────────────────────────
# B4.1 – Main test
# ─────────────────────────────────────────────
def test_b41():
    print("\n" + "=" * 60)
    print("B4.1 – FFD HEURISTIC DEMONSTRATION")
    print("=" * 60)

    C = 10.0
    # 12 workloads with varied sizes
    workloads = [6, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1]

    print(f"\nWorkloads : {workloads}")
    print(f"Capacity  : {C}")

    t0 = time.perf_counter()
    bins, rem = first_fit_decreasing(workloads, C)
    t1 = time.perf_counter()

    print_allocation(bins, rem, C, "FFD")
    print(f"\n  Time: {(t1-t0)*1000:.4f} ms")
    print(f"  Selection rule: Largest workload first; "
          f"place in first server with sufficient remaining capacity.")


# ─────────────────────────────────────────────
# B4.2 – Challenge case
# ─────────────────────────────────────────────
def test_b42():
    print("\n" + "=" * 60)
    print("B4.2 – CHALLENGE CASE: FFD vs EXACT")
    print("=" * 60)

    C = 10.0
    # Adversarial input for FFD: sizes that FFD packs sub-optimally
    # Workloads: six items of size 6, six items of size 4
    # Optimal: pack one 6 + one 4 = 10 → 6 servers
    # FFD: sorts → [6,6,6,6,6,6,4,4,4,4,4,4]
    #      6→S1, 6→S2, 6→S3, 6→S4, 6→S5, 6→S6
    #      then 4 each needs new server (rem=4 for all S1..S6, so FFD
    #      places 4 in S1 → S1 full; next 4 in S2 → S2 full; etc.
    #      → 6 servers total. Same as optimal!
    # Use a trickier case:
    # Sizes: 7, 5, 5, 5, 5, 3, 3, 3, 3, 3  (C=10)
    # Optimal: (7+3), (5+5), (5+5), (3+3+3+?) → Hmm.
    # Let's calculate manually:
    # Optimal: [7,3],[5,5],[5,5],[3,3,3+?] → [7,3]=10, [5,5]=10, [5,5]=10, [3,3,3]=9 → 4 bins
    # FFD order: 7,5,5,5,5,3,3,3,3,3
    # FFD: S1←7, 5→S1? rem=3<5 no→S2←5, 5→S1? no→S2? rem=5>=5→S2, 5→S3←5, 5→S3? rem=5→S3,
    #      3→S1 rem=3→place, 3→S2 rem=0 no→S3 rem=0 no→S4←3,
    #      3→S4, 3→S4? rem=4>=3→S4=9, 3→S5←3
    # FFD result: S1=[7,3], S2=[5,5], S3=[5,5], S4=[3,3,3], S5=[3] → 5 bins
    # Exact: [7,3],[5,5],[5,5],[3,3,3,?] - 4 bins works? [3,3,3]=9≤10 yes → 4 bins

    workloads_challenge = [7, 5, 5, 5, 5, 3, 3, 3, 3, 3]
    print(f"\nChallenge workloads: {workloads_challenge}")
    print(f"Capacity: {C}")

    bins_ffd, rem_ffd = first_fit_decreasing(workloads_challenge, C)
    opt_bins, opt_assign = exact_bin_packing(workloads_challenge, C)

    print_allocation(bins_ffd, rem_ffd, C, "FFD (Heuristic)")

    # Build exact display
    opt_rem = [C - sum(b) for b in opt_assign]
    print_allocation(opt_assign, opt_rem, C, "EXACT (Optimal)")

    print(f"\n  FFD used  : {len(bins_ffd)} servers")
    print(f"  Optimal   : {opt_bins} servers")
    if len(bins_ffd) > opt_bins:
        print(f"  ✗ FFD is SUBOPTIMAL by {len(bins_ffd) - opt_bins} server(s).")
        print(f"  Reason: FFD packed [7] into Server 1 alone (rem=3).")
        print(f"  The 5-unit workloads filled two servers (5+5=10 each),")
        print(f"  leaving no room to combine 3+3+3+3 efficiently.")
        print(f"  Optimal packs [7,3],[5,5],[5,5],[3,3,3,?] using one fewer server.")
    else:
        print(f"  FFD matched optimal for this instance.")


# ─────────────────────────────────────────────
# B4.3 – Production Decision Note
# ─────────────────────────────────────────────
def print_decision_note():
    print("\n" + "=" * 60)
    print("B4.3 – ALGORITHM ENGINEERING DECISION NOTE")
    print("=" * 60)
    print("""
  Problem: Assign N cloud workloads to servers at production scale.
  Chosen strategy: First Fit Decreasing (FFD)

  ┌─────────────────────────────────────────────────────────┐
  │ Why exhaustive search is unattractive at production scale│
  ├─────────────────────────────────────────────────────────┤
  │ Bin packing is NP-Hard. Exact search over all possible   │
  │ assignments of N workloads into k bins explores k^N     │
  │ states. For N=100 workloads this is astronomical.        │
  │ A production system receiving 1000 workloads/second      │
  │ cannot afford exponential latency.                       │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ What guarantee FFD provides                              │
  ├─────────────────────────────────────────────────────────┤
  │ FFD is proven to use at most (11/9)·OPT + 6/9 bins.    │
  │ For large N, this means at most ~22% more servers than  │
  │ the minimum. This is a WORST-CASE guarantee, not average.│
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ Computational advantage                                  │
  ├─────────────────────────────────────────────────────────┤
  │ FFD runs in O(N log N) time (dominated by the sort).    │
  │ For N=1000 workloads this requires ~10,000 operations   │
  │ vs ~10^300 for exhaustive search. Placement decisions    │
  │ are made in microseconds.                               │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ When an exact approach might still be appropriate        │
  ├─────────────────────────────────────────────────────────┤
  │ • Offline planning for ≤ 15–20 workloads where server  │
  │   costs dominate (e.g., bare-metal contracts).          │
  │ • Safety-critical systems where over-provisioning has   │
  │   safety or regulatory consequences.                     │
  │ • One-time migrations where optimal packing is worth    │
  │   extended computation time.                            │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │ Evidence to monitor before deployment                    │
  ├─────────────────────────────────────────────────────────┤
  │ 1. Server utilisation rate: target > 80% average.       │
  │ 2. Number of servers opened vs theoretical lower bound. │
  │ 3. Fraction of workloads requiring new server opens.    │
  │ 4. Tail latency of placement decisions (<1ms target).   │
  │ 5. Compare FFD output vs ILP solver on weekly samples  │
  │    to detect systematic drift from optimality.          │
  └─────────────────────────────────────────────────────────┘
""")


def main():
    print("=" * 60)
    print(" TASK B4 – BIN PACKING UNDER A PRODUCTION CONSTRAINT")
    print("=" * 60)

    test_b41()
    test_b42()
    print_decision_note()


if __name__ == "__main__":
    main()
