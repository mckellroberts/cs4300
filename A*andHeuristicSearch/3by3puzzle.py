from typing import List, Tuple

#Definition of State-Space and problem
class EightPuzzle:
    def __init__(self, initial: Tuple[int]):
        self.initial = initial
        self.goal = (1, 2, 3,
                     4, 5, 6,
                     7, 8, 0)  # solved state

    def InitialState(self) -> Tuple[int]:
        return self.initial

    def Actions(self, state: Tuple[int]) -> List[str]:
        actions = []
        index = state.index(0)  # blank
        row, col = divmod(index, 3)
        if row > 0: actions.append("Up")
        if row < 2: actions.append("Down")
        if col > 0: actions.append("Left")
        if col < 2: actions.append("Right")
        return actions

    def Transition(self, state: Tuple[int], action: str) -> Tuple[int]:
        index = state.index(0)
        row, col = divmod(index, 3)
        swap_index = index

        if action == "Up": swap_index = (row - 1) * 3 + col
        if action == "Down": swap_index = (row + 1) * 3 + col
        if action == "Left": swap_index = row * 3 + (col - 1)
        if action == "Right": swap_index = row * 3 + (col + 1)

        new_state = list(state)
        new_state[index], new_state[swap_index] = new_state[swap_index], new_state[index]
        return tuple(new_state)

    def GoalTest(self, state: Tuple[int]) -> bool:
        return state == self.goal

    def StepCost(self, state: Tuple[int], action: str, next_state: Tuple[int]) -> int:
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
                goal_row, goal_col = divmod(self.goal.index(v), 3)
                cur_row, cur_col = divmod(i, 3)
                dist += abs(goal_row - cur_row) + abs(goal_col - cur_col)
            return dist
        else:
            raise ValueError(f"Unknown heuristic: {variant}")
