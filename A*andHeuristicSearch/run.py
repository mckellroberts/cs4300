from puzzle import EightPuzzle
from searchCore import AStar

def printResult(result):
    print(f"Solution: {', '.join(result['solution'])}")
    print(f"Cost: {result['cost']}")
    print(f"Depth: {result['depth']}")
    print(f"Nodes Expanded: {result['nodesExpanded']}")
    print(f"Nodes Generated: {result['nodesGenerated']}")
    print(f"Max Frontier Size: {result['maxFrontierSize']}")
    print()  # blank line for readability

if __name__ == "__main__":
    # Example unsolved state
    initialState = ( 4, 1, 3,
                     2, 6, 8,
                     7, 5, 0)

    problem = EightPuzzle(initialState)

    for h in ["h0", "h1", "h2"]:
        print(f"\nRunning A* with {h}...")
        result = AStar(problem, heuristicVariant=h)
        printResult(result)
