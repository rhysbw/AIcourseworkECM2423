import time
from collections import deque
from PIL import Image
from datetime import datetime


def readMazeFile(fileName):
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
    """Finds the start and goal nodes in the maze.
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
    """Returns a list of valid neighboring locations.
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


def bfs(maze, start, goal):
    """Performs breadth-first search on the maze.
    @param maze: array representation of the maze
    @param start: position of start point
    @param goal: position of end point
    @return: path to end, amount of nodes explored, time taken to complete
    """
    startTime = time.time()
    queue = deque([start])
    visited = set()
    parent = {}
    nodesExplored = 0

    while queue:
        current = queue.popleft()
        nodesExplored += 1
        visited.add(current)

        if current == goal:
            # We found the goal node!
            endTime = time.time()
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path, nodesExplored, endTime - startTime, visited

        for n in get_valid_adjacent(maze, current):
            if n not in visited:
                queue.append(n)
                visited.add(n)
                parent[n] = current

    # We didn't find the goal node.
    return None, nodesExplored, time.time() - startTime, visited


def dfs(maze, start, goal):
    """Performs depth-first search on the maze."""
    startTime = time.time()
    stack = [start]
    visited = set()
    parent = {}
    nodesExplored = 0

    while stack:
        current = stack.pop()
        nodesExplored += 1
        visited.add(current)

        if current == goal:
            # We found the goal node!
            endTime = time.time()
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path, nodesExplored, endTime - startTime, visited

        for n in get_valid_adjacent(maze, current):
            if n not in visited:
                stack.append(n)
                visited.add(n)
                parent[n] = current

    # We didn't find the goal node.
    return None, nodesExplored, time.time() - startTime, visited


def pathOnMazeFile(maze, path, algorithm, mazeFile):
    """Marks the path on the maze and outputs it to a text file."""
    print('Generating Solution.txt')
    new_maze = []
    for row_index, row in enumerate(maze):
        new_row = []
        for col_index, cell in enumerate(row):
            if (row_index, col_index) in path:
                new_row.append('* ')
            else:
                new_row.append(cell + ' ')
        new_maze.append(new_row)

    with open(algorithm+ mazeFile + '.txt', 'w') as f:
        for row in new_maze:
            f.write(''.join(row) + '\n')


def visulizePath(maze, path, visited, algorithm, mazeFile):
    """Marks the path and visited cells on the maze and outputs it to an image file."""
    print('Generating Solution.png')
    height = len(maze)
    width = len(maze[0])
    img = Image.new('RGB', (width, height), 'white')
    pixels = img.load()

    for row_index, row in enumerate(maze):
        for col_index, cell in enumerate(row):
            if cell == '#':
                pixels[col_index, row_index] = (0, 0, 0)
            elif (row_index, col_index) in path:
                pixels[col_index, row_index] = (0, 0, 255)
            elif (row_index, col_index) in visited:
                pixels[col_index, row_index] = (255, 0, 0)

    img.save(algorithm + mazeFile + '.png')


def statsFile(path, execution_time, nodes_explored, algorithm, timestamp, mazeFile):
    with open('statistics.txt', 'a') as f:
        f.write(
            f'{timestamp}: Path found with {len(path)} steps in {execution_time:.4f} seconds. Witb {nodes_explored} nodes explored. Using {algorithm}. Using {mazeFile}' + '\n')

def makeFiles(path, execution_time, nodes_explored, algorithm, timestamp, mazeFile):
    statsFile(path, execution_time, nodes_explored, algorithm, timestamp, maze_file)
    visulizePath(maze, path, visited, algorithm, maze_file)
    pathOnMazeFile(maze, path, algorithm, maze_file)

if __name__ == '__main__':
    parent = {}
    # Select Maze file
    maze_file = input('Maze file nane or path [Press Enter for Default in code]: ')
    if maze_file == '':
        maze_file = 'maze-Large.txt'
    maze = readMazeFile(maze_file)
    start, goal = find_start_and_goal(maze)

    # Run Algorithm
    algorithmSelect = int(input("""\
1. Depth First Search
2. Breadth First Search
Choose Algorithm: """))
    algorithm = ""
    match algorithmSelect:
        case 1:
            path, nodes_explored, execution_time, visited = dfs(maze, start, goal)
            algorithm = "Depth First Search"
        case 2:
            path, nodes_explored, execution_time, visited = bfs(maze, start, goal)
            algorithm = "Breadth First Search"

    if path:
        timestamp = str(datetime.now())
        print(f'Path found with {len(path)} steps in {execution_time:.4f} seconds.')
        print(f'Explored {nodes_explored} nodes.')
        if input("Do you want the output files (Y/N): ") == 'Y':
            makeFiles(path, execution_time, nodes_explored, algorithm, timestamp, maze_file)


    else:
        print('No path found.')
