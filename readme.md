# Wolves and Chickens

This project attempts to find a way from an initial state to a goal state for the wolves and chickens problem. The steps taken are printed, and saved to an output file as well.

### State file structure:

```
[number of chickens on left bank],[number of wolves on left bank],[1 for boat on left bank, otherwise 0]
[number of chickens on right bank],[number of wolves on right bank],[1 for boat on right bank, otherwise 0]
```

#### Example

```
0,0,0
3,2,1
```

### Arguments structure:

```main.py [initial state file] [goal state file] [mode] [output file]```

Where `mode` is one of the following search algorithms:
* Breadth-first search: `bfs`
* Depth-first search: `dfs`
* Iterative deepening depth-first search: `iddfs`
* A-Star: `astar`

#### Example

```main.py start1.txt goal1.txt bfs output.txt```