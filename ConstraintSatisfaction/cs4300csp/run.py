import sys
import os
import time

# Assuming these modules are in the same directory as run.py
import cs4300_csp
import cs4300_csp_parser
from cs4300_csp import CSPSolver

def run_solver(filepath, heuristic):
    """
    Parses and solves a CSP file, then prints the results in a report format.
    """
    try:
        # Load the CSP problem
        vars, domains, constraints = cs4300_csp_parser.parse(filepath)
        print(f"Loading and solving {filepath} with {heuristic} heuristic...\n")

        # Initialize the solver with the chosen heuristic
        solver = CSPSolver(vars, domains, constraints)

        # Measure the runtime
        start_time = time.time()
        solution_found, solution = solver.solve_backtracking(heuristic=heuristic)
        end_time = time.time()

        runtime = end_time - start_time
        search_steps = solver.backtracks

        # Formalize the problem for the report
        report_vars = "\n".join([f"  - {v}: {list(domains[v])}" for v in sorted(vars)])
        report_cons = "\n".join([f"  - {c.get_description()}" for c in constraints])

        # Print the formal report
        print("-----------------------------------------------------------------------------------")
        print(f"Problem Description ({os.path.basename(filepath)})")
        print("-----------------------------------------------------------------------------------")
        print("Formalization <X, D, C>:")
        print("  X: Set of variables (see VARS in the .csp file)")
        print(f"  D: Domains for each variable:")
        print(f"  {report_vars}")
        print("  C: Constraints (see CONS in the .csp file)")
        print(f"  {report_cons}")
        print("\nHeuristics Discussion:")
        print(f"  Using: {heuristic if heuristic else 'None'}")
        print("  [Insert your discussion of MRV and LCV here.]")
        print("\nResults and Reflection:")
        print(f"  Search Steps (Backtracks): {search_steps}")
        print(f"  Runtime: {runtime:.4f} seconds")

        if solution_found:
            print("\n  Solution Found:")
            formatted_solution = {}
            for var, val in solution.items():
                category = ''.join(filter(str.isalpha, var))
                if category not in formatted_solution:
                    formatted_solution[category] = {}
                formatted_solution[category][var] = val
            
            print("  [Note: The numerical values correspond to your attribute mappings.]")
            for cat, vals in sorted(formatted_solution.items()):
                print(f"  {cat}:")
                for var, val in sorted(vals.items()):
                    print(f"    - {var}: {val}")

            print("\n  [Insert your reflection on solver performance here.]")
        else:
            print("\n  No solution found.")

    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found. Please make sure it exists in the 'instances/' directory.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Welcome to the Zebra Puzzle Solver.")
    
    heuristic_choice = input("Choose a heuristic (None, MRV, LCV): ")
    if heuristic_choice.upper() not in ["NONE", "MRV", "LCV"]:
        print("Invalid heuristic choice. Exiting.")
        sys.exit(1)
    heuristic = heuristic_choice.upper() if heuristic_choice.upper() != "NONE" else None

    print("\nChoose a puzzle to solve:")
    print("1. 3-House Variant")
    print("2. 5-House Variant")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        print("\nChoose an instance:")
        print("  a. threeHouseA.csp")
        print("  b. threeHouseB.csp")
        print("  c. threeHouseC.csp")
        instance_choice = input("Enter your choice (a, b, or c): ")
        
        if instance_choice == 'a':
            file_path = "instances/threeHouseA.csp"
        elif instance_choice == 'b':
            file_path = "instances/threeHouseB.csp"
        elif instance_choice == 'c':
            file_path = "instances/threeHouseC.csp"
        else:
            print("Invalid instance choice. Exiting.")
            sys.exit(1)
    elif choice == '2':
        print("\nChoose an instance:")
        print("  a. fiveHouseA.csp")
        print("  b. fiveHouseB.csp")
        instance_choice = input("Enter your choice (a or b): ")

        if instance_choice == 'a':
            file_path = "instances/fiveHouseA.csp"
        elif instance_choice == 'b':
            file_path = "instances/fiveHouseB.csp"
        else:
            print("Invalid instance choice. Exiting.")
            sys.exit(1)
    else:
        print("Invalid puzzle size choice. Exiting.")
        sys.exit(1)

    run_solver(file_path, heuristic)
