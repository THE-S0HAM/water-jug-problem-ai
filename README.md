# Water Jug Problem Solver

Sanjivani College of Engineering, Kopargaon. Department of Information Technology, AY 2026-27.
AI Part B Activity: design, implementation and evaluation of a search-based AI problem solver.

Team: Vaibhav Chavhan (UIT23M1029), Shruti Dabhade (UIT23F1030), Sayee Deshmukh (UIT23F1034), Soham Deshmukh (UIT23M1035).
Lab In-charge: Prof. Shubham Zanwar.

## What it does

You have two jugs with capacities `a` and `b` litres. The solver finds a sequence of fill, empty and pour operations that leaves exactly `t` litres in one jug. It uses BFS, DFS or A* search, and it runs a gcd check first so unsolvable inputs are rejected without searching.

- State: `(x, y)`, the litres in Jug A and Jug B. The start state is `(0, 0)`.
- Operators: Fill A, Fill B, Empty A, Empty B, Pour A -> B, Pour B -> A.
- Goal: `x == t` or `y == t`.
- Solvable when `t <= max(a, b)` and `t % gcd(a, b) == 0`.
- A* heuristic: `h = min(|x - t|, |y - t|)`.

## Requirements

Python 3.8+ with only the standard library. `matplotlib` is needed only for the optional chart.

## Usage

```powershell
python water_jug.py 3 5 4              # BFS (default)
python water_jug.py 3 5 4 --algo dfs
python water_jug.py 3 5 4 --algo astar
python water_jug.py 3 5 4 --algo all   # compare all three
python water_jug.py 4 6 5              # unsolvable input

python evaluate.py                     # comparison table for the 9 test inputs
python evaluate.py --plot              # also saves nodes_expanded.png
```

## Files

| File | Contents |
|------|----------|
| `water_jug.py` | `successors()`, `solvable()`, `bfs()`, `dfs()`, `astar()`, `build_path()`, `show()` and the CLI |
| `evaluate.py` | Runs the report's nine test cases and prints steps / nodes expanded |
