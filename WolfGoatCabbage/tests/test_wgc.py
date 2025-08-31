import pytest
from wgc import initial_state, goal_state, is_valid, successors, State, LEFT, RIGHT

def test_initial_and_goal_states():
    assert initial_state() == State(LEFT, LEFT, LEFT, LEFT)
    assert goal_state() == State(RIGHT, RIGHT, RIGHT, RIGHT)

def test_validity_checker():
    # Valid: everyone left
    assert is_valid(State(LEFT, LEFT, LEFT, LEFT))
    # Invalid: wolf & goat alone on left
    assert not is_valid(State(RIGHT, LEFT, LEFT, RIGHT))
    # Invalid: goat & cabbage alone on right
    assert not is_valid(State(LEFT, RIGHT, RIGHT, RIGHT))

def test_successors_are_valid():
    start = initial_state()
    for action, next_state in successors(start):
        assert is_valid(next_state), f"Invalid successor from {start} via {action}"
