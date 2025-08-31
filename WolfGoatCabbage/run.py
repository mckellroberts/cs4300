# run.py
import argparse
from wgc import initialState, goalState, successors, formatState
from searchCore import bfs, ids

def run(domain, algo):
    start = initialState()
    goal_test = lambda s: s == goalState()

    if algo == "bfs":
        path, stats = bfs(start, goal_test, successors)
    elif algo == "ids":
        path, stats = ids(start, goal_test, successors)
    else:
        raise ValueError("Unknown algorithm")

    print(f"Domain: {domain} | Algorithm: {algo.upper()}")
    if path is None:
        print("No solution found.")
        return

    print(f"Solution cost: {len(path)} | Depth: {len(path)}")
    print(f"Nodes generated: {stats.generated} | Nodes expanded: {stats.expanded} | Max frontier: {stats.maxFrontier}")
    print("Path:")
    current = start
    for i, (action, state) in enumerate(path, 1):
        print(f"  {i}) {action:12} {formatState(current)} -> {formatState(state)}")
        current = state

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default="WGC")
    parser.add_argument("--algo", choices=["bfs", "ids"], required=True)
    args = parser.parse_args()
    run(args.domain, args.algo)
