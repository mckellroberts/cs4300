from collections import namedtuple

# Represent state as a tuple (Boat, Wolf, Goat, Cabbage)
# Each can be 'L' or 'R'
State = namedtuple("State", ["B", "W", "G", "C"])

LEFT, RIGHT = "L", "R"

def initialState():
    return State(RIGHT, LEFT, LEFT, RIGHT)

def goalState():
    return State(RIGHT, RIGHT, RIGHT, RIGHT)

def isValid(state: State) -> bool:
    """Check constraints: wolf/goat and goat/cabbage not left alone."""
    # Wolf eats goat
    if state.W == state.G and state.B != state.W:
        return False
    # Goat eats cabbage
    if state.G == state.C and state.B != state.G:
        return False
    return True

def successors(state: State):
    """Generate valid next states with action descriptions."""
    moves = []
    opposite = {LEFT: RIGHT, RIGHT: LEFT}

    # Boat always moves
    newB = opposite[state.B]

    # Boat moves alone
    newState = State(newB, state.W, state.G, state.C)
    if isValid(newState):
        moves.append(("Return alone" if newB == LEFT else "Move alone", newState))

    # Boat takes Wolf
    if state.B == state.W:
        newState = State(newB, newB, state.G, state.C)
        if isValid(newState):
            moves.append(("Take Wolf", newState))

    # Boat takes Goat
    if state.B == state.G:
        newState = State(newB, state.W, newB, state.C)
        if isValid(newState):
            moves.append(("Take Goat", newState))

    # Boat takes Cabbage
    if state.B == state.C:
        newState = State(newB, state.W, state.G, newB)
        if isValid(newState):
            moves.append(("Take Cabbage", newState))

    return moves

def formatState(state):
    """Return state as a compact tuple-like string, e.g. (L,L,R,L)."""
    return f"({state.B}, {state.W}, {state.G}, {state.C})"