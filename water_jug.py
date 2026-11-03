"""Water Jug Problem Solver using BFS, DFS and A* search.

Usage:
    python water_jug.py A B T [--algo bfs|dfs|astar|all]

Example:
    python water_jug.py 3 5 4
    python water_jug.py 3 5 4 --algo all
"""
import argparse
import heapq
import sys
from collections import deque
from math import gcd

START = (0, 0)


def successors(state, cap):
    """Return list of (action, new_state) for the six production rules."""
    x, y = state
    a, b = cap
    res = [("Fill Jug A", (a, y)), ("Fill Jug B", (x, b)),
           ("Empty Jug A", (0, y)), ("Empty Jug B", (x, 0))]
    t = min(x, b - y)
    res.append(("Pour A -> B", (x - t, y + t)))
    t = min(y, a - x)
    res.append(("Pour B -> A", (x + t, y - t)))
    return [(n, s) for n, s in res if s != state]


def solvable(cap, target):
    """gcd test: target must fit in the larger jug and be a multiple of gcd(a, b)."""
    a, b = cap
    return target <= max(a, b) and target % gcd(a, b) == 0


def is_goal(state, target):
    return target in state


def build_path(parent, goal):
    """Rebuild the list of (action, state) from the start to the goal."""
    path, s = [], goal
    while s is not None:
        prev, act = parent[s]
        path.append((act, s))
        s = prev
    return path[::-1]


def bfs(cap, target):
    parent = {START: (None, "Start")}
    q, explored = deque([START]), 0
    while q:
        s = q.popleft()
        explored += 1
        if is_goal(s, target):
            return build_path(parent, s), explored, len(parent)
        for act, n in successors(s, cap):
            if n not in parent:
                parent[n] = (s, act)
                q.append(n)
    return None, explored, len(parent)


def dfs(cap, target):
    parent = {START: (None, "Start")}
    stack, explored = [START], 0
    while stack:
        s = stack.pop()
        explored += 1
        if is_goal(s, target):
            return build_path(parent, s), explored, len(parent)
        for act, n in successors(s, cap):
            if n not in parent:
                parent[n] = (s, act)
                stack.append(n)
    return None, explored, len(parent)


def heuristic(state, target):
    """Distance of the closer jug content from the target (not proven admissible)."""
    x, y = state
    return min(abs(x - target), abs(y - target))


def astar(cap, target):
    parent = {START: (None, "Start")}
    g = {START: 0}
    pq = [(heuristic(START, target), START)]  # ties on f broken by state tuple
    closed, explored = set(), 0
    while pq:
        _, s = heapq.heappop(pq)
        if s in closed:
            continue
        closed.add(s)
        explored += 1
        if is_goal(s, target):
            return build_path(parent, s), explored, len(parent)
        for act, n in successors(s, cap):
            ng = g[s] + 1
            if n not in g or ng < g[n]:
                g[n] = ng
                parent[n] = (s, act)
                heapq.heappush(pq, (ng + heuristic(n, target), n))
    return None, explored, len(parent)


ALGORITHMS = {"bfs": bfs, "dfs": dfs, "astar": astar}


def solve(a, b, t, algo):
    """Run one algorithm. Returns (path, explored, generated) or None if unsolvable."""
    if not solvable((a, b), t):
        return None
    return ALGORITHMS[algo]((a, b), t)


def show(name, result):
    path, explored, generated = result
    if path is None:
        print(f"[{name}] no solution found (explored {explored} nodes)")
        return
    print(f"[{name}] steps = {len(path) - 1}, nodes expanded = {explored}, "
          f"states generated = {generated}")
    for i, (act, s) in enumerate(path):
        print(f"  Step {i:2d}: {act:<12} -> {s}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Water Jug Problem Solver")
    p.add_argument("a", type=int, help="capacity of Jug A (litres)")
    p.add_argument("b", type=int, help="capacity of Jug B (litres)")
    p.add_argument("t", type=int, help="target quantity (litres)")
    p.add_argument("--algo", choices=["bfs", "dfs", "astar", "all"], default="bfs")
    args = p.parse_args(argv)

    if min(args.a, args.b, args.t) <= 0:
        print("Error: capacities and target must be positive integers.")
        return 1

    print(f"Jug A = {args.a} L, Jug B = {args.b} L, Target = {args.t} L\n")
    if not solvable((args.a, args.b), args.t):
        print("No solution: target is not a multiple of gcd(a, b) "
              "or exceeds jug capacity.")
        return 0

    algos = ["bfs", "dfs", "astar"] if args.algo == "all" else [args.algo]
    for algo in algos:
        show(algo.upper() if algo != "astar" else "A*",
             ALGORITHMS[algo]((args.a, args.b), args.t))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
