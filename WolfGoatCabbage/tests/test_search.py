from wgc import initial_state, goal_state, successors
from search_core import bfs, ids

def test_bfs_finds_solution():
    start = initial_state()
    goal_test = lambda s: s == goal_state()
    path, stats = bfs(start, goal_test, successors)

    assert path is not None
    assert len(path) == 7  # known minimal solution cost
    assert len(path) == len(path)  # depth = cost
    assert stats.generated > 0
    assert stats.expanded > 0

def test_ids_finds_solution():
    start = initial_state()
    goal_test = lambda s: s == goal_state()
    path, stats = ids(start, goal_test, successors, max_depth=15)

    assert path is not None
    assert len(path) == 7
    assert stats.generated > 0
