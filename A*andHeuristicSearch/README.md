Terminal run command: python3 run.py

This code goes over the solution of the 8 puzzle using a Heuristic A* search.

puzzle.py defines the 8 puzzle's initial state, actions, transition states, goal states, and the cost of each move.

searchCore.py builds the A* search function and defines the different heuristic levels; h0, h1, h2, respectfully.

run.py passes in the initial state and gives the results of running A* Search at each Heuristic Level.