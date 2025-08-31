This is my projects structure:
WolfGoatCabbage/
  README.md         # this file
  wgc.py            # domain definition (states, actions, transitions)
  search_core.py    # BFS and IDS implementations
  run.py            # entry point
  tests/            

How to run, from inside WolfGoatCabbage folder
    python3 run.py --domain WGC --algo bfs
    #For the bfs search 
    python3 run.py --domain WGC --algo ids
    #For the ids search

The output should look like:
    Domain: WGC | Algorithm: BFS
    Solution cost: 7 | Depth: 7
    Nodes generated: 23 | Nodes expanded: 15 | Max frontier: 6
    Path:
    1) Move Goat       (L,L,L,L) -> (R,L,R,L)
    2) Return alone    (R,L,R,L) -> (L,L,R,L)
    ...
