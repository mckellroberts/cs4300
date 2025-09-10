import heapq

def AStar(threeByThree, heuristicVariant="h0"):
    initial = threeByThree.InitialState()
    frontier = [(threeByThree.Heuristic(initial, heuristicVariant), 0, initial, [])]
    bestG = {initial: 0} #Best path based on cost, if cost is all uniform, than first quickest path
    explored = set()

    nodesExpanded = 0
    nodesGenerated = 0
    maxFrontierSize = 1

    while frontier:
        f, g, state, path = heapq.heappop(frontier)

        if threeByThree.GoalTest(state):
            return {
                "solution": path,
                "cost": g,
                "depth": len(path),
                "nodesExpanded": nodesExpanded,
                "nodesGenerated": nodesGenerated,
                "maxFrontierSize": maxFrontierSize,
            }

        if state in explored:
            continue
        explored.add(state)
        nodesExpanded += 1

        #Expands tree based on available actions
        for action in threeByThree.Actions(state):
            nextState = threeByThree.Transition(state, action)
            newG = g + threeByThree.StepCost(state, action, nextState)
            newF = newG + threeByThree.Heuristic(nextState, heuristicVariant)

            #If new path isn't more cost effective, cut off
            if nextState not in bestG or newG < bestG[nextState]:
                bestG[nextState] = newG
                nodesGenerated += 1
                heapq.heappush(frontier, (newF, newG, nextState, path + [action]))
                maxFrontierSize = max(maxFrontierSize, len(frontier))

    return None  # failure
