Zebra Puzzle Solver
1. Introduction
This project implements a Constraint Satisfaction Problem (CSP) solver to find a solution for variants of the classic Zebra Puzzle. The solver utilizes a backtracking search algorithm with forward checking and can be configured to use various heuristics to improve performance.

2. Problem Formalization
The Zebra Puzzle is formalized as a Constraint Satisfaction Problem, represented by the triplet \<X,D,C.

Variables (X): A set of variables representing the position of each attribute (e.g., PosRed, PosJohn, PosDog).

Domains (D): The domain for each variable is the set of possible house positions. For the 3-house variant, the domain is 0,1,2, and for the 5-house variant, it is 0,1,2,3,4.

Constraints (C): A set of constraints linking the variables. The problem constraints include:

alldiff: Ensures that all attributes of a given type (e.g., all pets) are in different houses.

eq: Equates the positions of two attributes (e.g., eq(PosRed, PosDog)).

table: Defines relationships between variables based on a set of allowed tuples, used for "next to" constraints.

3. Project Structure
The project is organized into the following files and directories:

run.py: The main script that serves as the user interface. It prompts the user for the puzzle instance and heuristic to use, then calls the solver.

cs4300_csp.py: Contains the core CSPSolver class, which implements the backtracking search algorithm and the chosen heuristics. It also defines the various constraint classes.

cs4300_csp_parser.py: The parser responsible for reading the custom .csp files and translating them into the internal CSP data structures.

instances/: A directory containing all the .csp files for the different Zebra Puzzle instances.

4. Running the Solver
To run the solver, navigate to the project directory in your terminal and execute the run.py script.

python run.py

The script will guide you through a simple command-line interface. Follow the prompts to select your preferences for each run.

Step-by-Step Usage:

Choose a Heuristic: Enter None, MRV, or LCV when prompted.

Choose a Puzzle Variant: Enter 1 for the 3-house variant or 2 for the 5-house variant.

Choose a Specific Instance: Enter the letter corresponding to the .csp file you wish to run (e.g., a, b, or c).

The program will then display a detailed report, including the problem formalization, a discussion of the chosen heuristic, and the performance results, such as the number of backtracks and the total runtime.

5. Implemented Heuristics
The backtracking search can be configured with the following heuristics to improve efficiency:

None (Standard Backtracking): Variables are selected in their default order, and values are tried in their natural order from the domain. This serves as the baseline for performance comparison.

MRV (Most-Constrained Variable): The solver always selects the next variable to assign that has the fewest remaining legal values in its domain. This prunes the search space earlier by making more critical decisions first.

LCV (Least-Constraining Value): When selecting a value for a variable, the solver chooses the one that rules out the fewest options for neighboring variables. This aims to keep the maximum number of options available for future assignments.

6. Solver Performance
The output of the program provides key metrics to evaluate the performance of each heuristic:

Search Steps (Backtracks): The number of times the algorithm had to backtrack due to an inconsistent assignment. A lower number indicates a more efficient search.

Runtime: The total time taken to find a solution, measured in seconds.

These metrics allow for a direct comparison of the effectiveness of MRV and LCV against the standard backtracking approach.