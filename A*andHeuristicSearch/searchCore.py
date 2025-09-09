This file contains your A* and UCS implementations, using heapq for the priority queue.

Key elements:

frontier: min-heap storing (f, g, state, path)

best_g: dict tracking best known cost for each visited state

expanded_count, generated_count, max_frontier_size for metrics

AStar(problem, heuristic_variant)

UniformCostSearch(problem) (A* with h0 = 0)