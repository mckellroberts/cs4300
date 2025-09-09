from typing import List, Tuple

#Definition of State-Space and problem
class EightPuzzle:
    def __init__(self, initial: Tuple[int]):
        self.initial = initial
        self.goal = (1, 2, 3,
                     4, 5, 6,
                     7, 8, 0)  # solved state

    #Random list of 0-8
    def InitialState(self) -> Tuple[int]:
        return self.initial

    #Adds legal actions, no going outside of the 3x3
    def Actions(self, state: Tuple[int]) -> List[str]:
        actions = []
        index = state.index(0)  # blank
        row, col = divmod(index, 3)
        if row > 0: actions.append("Up")
        if row < 2: actions.append("Down")
        if col > 0: actions.append("Left")
        if col < 2: actions.append("Right")
        return actions

    #Switches the tiles/numbers and makes new state
    def Transition(self, state: Tuple[int], action: str) -> Tuple[int]:
        index = state.index(0)
        row, col = divmod(index, 3)
        swapIndex = index

        if action == "Up": swapIndex = (row - 1) * 3 + col
        if action == "Down": swapIndex = (row + 1) * 3 + col
        if action == "Left": swapIndex = row * 3 + (col - 1)
        if action == "Right": swapIndex = row * 3 + (col + 1)

        newState = list(state)
        newState[index], newState[swapIndex] = newState[swapIndex], newState[index]
        return tuple(newState)

    #Checks to see if Goal State is achieved.
    def GoalTest(self, state: Tuple[int]) -> bool:
        return state == self.goal

    #Each step will only ever cost 1.
    def StepCost(self, state: Tuple[int], action: str, nextState: Tuple[int]) -> int:
        return 1

    # --- Heuristics ---
    def Heuristic(self, state: Tuple[int], variant="h0") -> int:
        if variant == "h0":  # UCS baseline
            return 0
        elif variant == "h1":  # Misplaced tiles
            return sum(1 for i, v in enumerate(state) if v != 0 and v != self.goal[i])
        elif variant == "h2":  # Manhattan distance
            dist = 0
            for i, v in enumerate(state):
                if v == 0: continue
                goalRow, goalCol = divmod(self.goal.index(v), 3)
                curRow, curCol = divmod(i, 3)
                dist += abs(goalRow - curRow) + abs(goalCol - curCol)
            return dist
        else:
            raise ValueError(f"Unknown heuristic: {variant}")
