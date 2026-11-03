"""Run BFS, DFS and A* on the report's nine test inputs and print a comparison.

Usage:
    python evaluate.py          # print the table
    python evaluate.py --plot   # also save nodes_expanded.png (needs matplotlib)
"""
import argparse

from water_jug import solve

TESTS = [
    (3, 5, 4), (4, 3, 2), (5, 7, 6), (7, 11, 6), (8, 13, 9), (12, 17, 10),
    (4, 6, 5), (6, 9, 4), (5, 3, 7),
]
ALGOS = [("bfs", "BFS"), ("dfs", "DFS"), ("astar", "A*")]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--plot", action="store_true", help="save a bar chart of nodes expanded")
    args = p.parse_args()

    print(f"{'Jugs (A, B)':<12} {'Target':>6}  " + "  ".join(f"{n:>12}" for _, n in ALGOS))
    print("-" * 56)
    totals = {k: 0 for k, _ in ALGOS}
    chart = []  # (label, [nodes per algo]) for solvable cases
    for a, b, t in TESTS:
        cells, nodes = [], []
        for key, _ in ALGOS:
            r = solve(a, b, t, key)
            if r is None or r[0] is None:
                cells.append("No solution")
            else:
                path, explored, _ = r
                cells.append(f"{len(path) - 1} / {explored}")
                totals[key] += explored
                nodes.append(explored)
        if nodes:
            chart.append((f"({a},{b}) t={t}", nodes))
        print(f"{f'({a}, {b})':<12} {t:>6}  " + "  ".join(f"{c:>12}" for c in cells))

    print("\nCells show steps / nodes expanded.")
    print("Total nodes expanded on solvable cases: "
          + ", ".join(f"{n} = {totals[k]}" for k, n in ALGOS))

    if args.plot:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not installed; run: pip install matplotlib")
            return
        labels = [c[0] for c in chart]
        width = 0.27
        xs = range(len(labels))
        for i, (_, name) in enumerate(ALGOS):
            plt.bar([x + (i - 1) * width for x in xs], [c[1][i] for c in chart],
                    width, label=name)
        plt.xticks(list(xs), labels, rotation=20)
        plt.ylabel("Nodes expanded")
        plt.title("Nodes expanded by BFS, DFS and A*")
        plt.legend()
        plt.tight_layout()
        plt.savefig("nodes_expanded.png", dpi=150)
        print("Saved nodes_expanded.png")


if __name__ == "__main__":
    main()
