from puzzle import EightPuzzle
from searchCore import AStar

if __name__ == "__main__":
    # Example unsolved state
    initial_state = (4, 1, 3,
                     2, 6, 8,
                     7, 5, 0)

    problem = EightPuzzle(initial_state)

    for h in ["h0", "h1", "h2"]:
        print(f"\nRunning A* with {h}...")
        result = AStar(problem, heuristicVariant=h)
        print(result)
