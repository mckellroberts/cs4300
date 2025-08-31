from collections import deque

class SearchStats:
    def __init__(self):
        self.generated = 0
        self.expanded = 0
        self.maxFrontier = 0

def bfs(start, goalTest, successors):
    frontier = deque([(start, [], 0)])  # (state, path, depth)
    explored = set()
    stats = SearchStats()

    while frontier:
        stats.maxFrontier = max(stats.maxFrontier, len(frontier))
        state, path, depth = frontier.popleft()

        if state in explored:
            continue
        explored.add(state)
        stats.expanded += 1

        if goalTest(state):
            return path, stats

        for action, nextState in successors(state):
            if nextState not in explored:
                stats.generated += 1
                frontier.append((nextState, path + [(action, nextState)], depth + 1))
    return None, stats

def dls(state, goalTest, successors, limit, path, stats, visited):
    """Recursive depth-limited search used by IDS."""
    if goalTest(state):
        return path, True
    if limit == 0:
        return None, False

    visited.add(state)
    cutoffOccurred = False
    stats.expanded += 1

    for action, nextState in successors(state):
        stats.generated += 1
        if nextState not in visited:
            result, cutoff = dls(nextState, goalTest, successors, limit - 1,
                                 path + [(action, nextState)], stats, visited)
            if result is not None:
                return result, True
            if cutoff:
                cutoffOccurred = True
    visited.remove(state)
    return None, cutoffOccurred

def ids(start, goal_test, successors, max_depth=50):
    stats = SearchStats()
    for depth in range(max_depth + 1):
        result, found = dls(start, goal_test, successors, depth, [], stats, set())
        stats.max_frontier = max(stats.max_frontier, len(stats.__dict__))
        if result is not None:
            return result, stats
    return None, stats
