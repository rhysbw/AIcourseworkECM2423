import time
import heapq
from collections import deque
from datetime import datetime


def read_maze_file(fileName):
    """
    Reads in a maze file and returns a 2D list representing the maze.
    @param fileName: name and location of Maze file
    @return: Array representation of the maze
    """
    mazeArray = []
    try:
        with open(fileName, 'r') as f:
            for line in f:
                if line.strip():  # check if line has content - error catches empty lines within the maze files
                    mazeArray.append(list(line.strip().split()))  # makes one list for every line of maze, and removes
                    # any spaces
    except:
        print("Invalid maze file")

    return mazeArray


def find_start_and_goal(maze):
    """
    Finds the start and goal nodes in the maze.
    @param maze: the array representation of the maze
    @return: startLocation of the maze, and end position of the maze
    """
    try:
        startPoint = (0, maze[0].index("-"))
        goalPoint = (len(maze) - 1, maze[-1].index("-"))
        return startPoint, goalPoint
    except:
        print("Invalid Maze File, could not locate start or end of maze")


def is_valid_location(maze, location):
    """
    Checks if a location is a valid path in the maze.
    @param maze: Array representation of the maze
    @param location: Row and Colum of the char in the maze
    @return: Boolean: based on if location is valid
    """
    row, col = location
    if row < 0 or row >= len(maze) or col < 0 or col >= len(
            maze[0]):  # checks if location actually resides within the maze space
        return False
    if maze[row][col] == '#':  # checks if is a wall or a valid movable space
        return False
    return True


def get_valid_adjacent(maze, location):
    """
    Returns a list of valid neighboring locations.
    @param maze: Array representation of the maze
    @param location: Row and Colum of the char in the maze
    @return: list of valid locations
    """
    row, col = location
    adjacent = [(row - 1, col), (row, col + 1), (row + 1, col),
                (row, col - 1)]  # list of all spaces next to current pos
    validPos = []
    # checks all adjacent locations to see which are valid
    for n in adjacent:
        if is_valid_location(maze, n):
            validPos.append(n)
    return validPos


def reveal_path(current, start, parent):
    """
    Returns a list of coordinates on the path
    @param start: coordinates of starting point
    @param parent: parent node for backtracking
    @return: list of valid locations
    """
    path = []
    while current != start:
        # reads path taken by checking which node was a parent of the current (starting at end point)
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    return path


def depth_first_search(maze, start, goal):
    """
    Performs depth-first search on the maze.
    @param maze: array representation of the maze
    @param start: position of start point
    @param goal: position of end point
    @return: path taken, number of nodes explored, time taken, coords of visited positions
    """
    startTime = time.time()  # for measuring time taken to find path
    stack = [start]
    visitedNodes = set()  # to allow not going back to previously visited node
    parent = {}  # to allow for backtracking between nodes to find path
    nodesExplored = 0

    while stack:
        current = stack.pop()  # sets the current nodes as the node at the top of the stack
        nodesExplored += 1
        visitedNodes.add(current)  # adds to list of visited nodes

        if current == goal:
            endTime = time.time()  # completed time
            path = reveal_path(current, start, parent)
            return path, nodesExplored, endTime - startTime, visitedNodes

        # checks for nodes that are valid and have not been visited and adds to top of stack
        for n in get_valid_adjacent(maze, current):
            if n not in visitedNodes:
                stack.append(n)
                parent[n] = current
    return None, nodesExplored, time.time() - startTime, visitedNodes


def breadth_first_search(maze, start, goal):
    """Performs breadth-first search on the maze.
    @param maze: array representation of the maze
    @param start: position of start point
    @param goal: position of end point
    @return: path to end, amount of nodes explored, time taken to complete, coords of visitedNodes positions
    """
    startTime = time.time()  # for measuring time taken to find path
    queue = deque([start])
    visitedNodes = set()  # to allow not going back to previously visitedNodes node
    parent = {}  # to allow for backtracking between nodes to find path
    nodesExplored = 0

    # queue is used instead of stack
    while queue:
        current = queue.popleft()  # sets the current node as the next node in queue
        nodesExplored += 1
        visitedNodes.add(current)  # adds to list of visitedNodes nodes

        if current == goal:
            endTime = time.time()  # completed time
            return reveal_path(current, start, parent), nodesExplored, endTime - startTime, visitedNodes

        # checks for nodes that are valid and have not been visitedNodes and adds to back of queue
        for n in get_valid_adjacent(maze, current):
            if n not in visitedNodes:
                queue.append(n)
                parent[n] = current

    return None, nodesExplored, time.time() - startTime, visitedNodes


def heuristic_cost(node, goal):
    """
    This is calculates the heuristic cost, currently the Manhattan distance as is used in Maze searches
    @param node: coordinates of the node
    @param goal: position of end point
    @return: path taken, number of nodes explored, time taken, coords of visited positions
    """
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def a_star_search(maze, start, goal):
    """
    Performs A* search on the maze.
    @param maze: array representation of the maze
    @param start: position of start point
    @param goal: position of end point
    @return: path taken, number of nodes explored, time taken, coords of visited positions
    """
    startTime = time.time()  # for measuring time taken to find path
    visitedNodes = set()  # to allow not going back to previously visited node
    parent = {}  # to allow for backtracking between nodes to find path
    nodesExplored = 0

    # heap with starting node and its cost (heuristic + path cost)
    heap = [(0, start)]
    heapq.heapify(heap)

    # dict to store the cost of each node in the path (the G score)
    costPath = {start: 0}

    while heap:
        currentCost, current = heapq.heappop(heap)  # pop node with the lowest cost from heap
        nodesExplored += 1
        visitedNodes.add(current)

        if current == goal:
            endTime = time.time()  # completed time
            path = reveal_path(current, start, parent)
            return path, nodesExplored, endTime - startTime, visitedNodes

        # checks for nodes that are valid and have not been visited and adds to heap
        for n in get_valid_adjacent(maze, current):
            # calculate cost of reaching adjacent node
            newCost = costPath[current] + 1  # each step has cost 1

            # if the adjacent node has not been visited yet or the new cost is less than its current cost
            if n not in visitedNodes or newCost < costPath[n]:
                costPath[n] = newCost  # update its cost

                # add the node to heap with its total cost (heuristic + path cost)
                heapq.heappush(heap, (newCost + heuristic_cost(n, goal), n))

                parent[n] = current  # update its parent for backtracking
    return None, nodesExplored, time.time() - startTime, visitedNodes


def path_on_maze_file(maze, path, algorithm, mazeFile):
    """
    Marks the path on the maze and outputs it to a text file.
    @param maze: array representation of the maze
    @param path: [row][colum] position of the path taken
    @param algorithm: algorithm used to generate said path
    @param mazeFile: name of file used as maze input
    """
    print('Generating txt map')
    new_maze = []
    for row_index, row in enumerate(maze):
        new_row = []
        for col_index, cell in enumerate(row):
            if (row_index, col_index) in path:
                new_row.append('* ')
            else:
                new_row.append(cell + ' ')
        new_maze.append(new_row)

    with open(algorithm + mazeFile + '.txt', 'w') as f:
        for row in new_maze:
            f.write(''.join(row) + '\n')


def stats_file(path, execution_time, nodes_explored, algorithm, timestamp, mazeFile):
    """
    Generates/adds text file and enters all the statistics as a new line in file
    @param path: [row][colum] position of the path taken
    @param execution_time: time in seconds to find path
    @param nodes_explored: number of total nodes visited
    @param algorithm: algorithm used to generate said path
    @param timestamp: datetime of [NOW] to be used for files saving
    @param mazeFile: name of file used as maze input
    """
    with open('statistics.txt', 'a') as f:
        f.write(
            f'{timestamp}: Path found with {len(path)} steps in {execution_time:.4f} seconds. With {nodes_explored} nodes explored. Using {algorithm}. Using {mazeFile}' + '\n')


def make_files(path, execution_time, nodes_explored, algorithm, timestamp, mazeFile):
    """
    Generates all files
    @param path: [row][colum] position of the path taken
    @param execution_time: time in seconds to find path
    @param nodes_explored: number of total nodes visited
    @param algorithm: algorithm used to generate said path
    @param timestamp: datetime of [NOW] to be used for files saving
    @param mazeFile: name of file used as maze input
    """
    stats_file(path, execution_time, nodes_explored, algorithm, timestamp, mazeFile)
    path_on_maze_file(maze, path, algorithm, maze_file)


if __name__ == '__main__':
    # Select Maze file
    maze_file = input('Maze file nane or path [Press Enter for Default in code]: ')
    if maze_file == '':
        maze_file = 'maze-Medium.txt'
    maze = read_maze_file(maze_file)
    start, goal = find_start_and_goal(maze)

    # Run Algorithm
    algorithmSelect = int(input("""
1. Depth First Search
2. Breadth First Search
3. A* Search
Choose Algorithm: """))
    algorithm = ""
    match algorithmSelect:
        case 1:
            path, nodes_explored, execution_time, visited = depth_first_search(maze, start, goal)
            algorithm = "Depth First Search"
        case 2:
            path, nodes_explored, execution_time, visited = breadth_first_search(maze, start, goal)
            algorithm = "Breadth First Search"
        case 3:
            path, nodes_explored, execution_time, visited = a_star_search(maze, start, goal)
            algorithm = "A* search"

    # if a path was located
    if path:
        timestamp = str(datetime.now())
        print(f'Path found with {len(path)} steps in {execution_time:.4f} seconds.')
        print(f'Explored {nodes_explored} nodes.')
        if input("Do you want the output files - This can take a while for larger mazes (Y/N): ") == 'Y':
            make_files(path, execution_time, nodes_explored, algorithm, timestamp, maze_file)
        if input("Do you want the path as a list of coordinates (Y/N): ") == 'Y':
            print(path)
    else:
        print('No path found.')
