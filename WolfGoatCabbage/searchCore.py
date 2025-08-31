from collections import deque

class SearchStats:
    def __init__(self):
        self.generated = 0
        self.expanded = 0
        self.max_frontier = 0

def bfs(start, goal_test, successors):
    frontier = deque([(start, [], 0)])  # (state, path, depth)
    explored = set()
    stats = SearchStats()

    while frontier:
        stats.max_frontier = max(stats.max_frontier, len(frontier))
        state, path, depth = frontier.popleft()

        if state in explored:
            continue
        explored.add(state)
        stats.expanded += 1

        if goal_test(state):
            return path, stats

        for action, next_state in successors(state):
            if next_state not in explored:
                stats.generated += 1
                frontier.append((next_state, path + [(action, next_state)], depth + 1))
    return None, stats

def dls(state, goal_test, successors, limit, path, stats, visited):
    """Recursive depth-limited search used by IDS."""
    if goal_test(state):
        return path, True
    if limit == 0:
        return None, False

    visited.add(state)
    cutoff_occurred = False
    stats.expanded += 1

    for action, next_state in successors(state):
        stats.generated += 1
        if next_state not in visited:
            result, cutoff = dls(next_state, goal_test, successors, limit - 1,
                                 path + [(action, next_state)], stats, visited)
            if result is not None:
                return result, True
            if cutoff:
                cutoff_occurred = True
    visited.remove(state)
    return None, cutoff_occurred

def ids(start, goal_test, successors, max_depth=50):
    stats = SearchStats()
    for depth in range(max_depth + 1):
        result, found = dls(start, goal_test, successors, depth, [], stats, set())
        stats.max_frontier = max(stats.max_frontier, len(stats.__dict__))
        if result is not None:
            return result, stats
    return None, stats
