import time
from collections import deque
from PIL import Image, ImageDraw


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
    if row < 0 or row >= len(maze) or col < 0 or col >= len(maze[0]):  # checks if location actually resides within the maze space
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
    adjacent = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]  # list of all spaces next to current pos
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
def visulizePath(maze, visited, path):

    # Define colors for drawing
    WALL_COLOR = (0, 0, 0)
    FREE_COLOR = (255, 255, 255)
    VISITED_COLOR = (159, 43, 104)
    PATH_COLOR = (0, 255, 0)

    # Convert maze list to an image
    img_width, img_height = len(maze[0]), len(maze)
    img = Image.new('RGB', (img_width, img_height))
    draw = ImageDraw.Draw(img)
    for y in range(img_height):
        for x in range(img_width):
            if maze[y][x] == '#':
                draw.rectangle([(x, y), (x + 1, y + 1)], fill=WALL_COLOR)
            else:
                draw.rectangle([(x, y), (x + 1, y + 1)], fill=FREE_COLOR)

    # Mark visited cells in the image


    # Mark path cells in the image
    for cell in path:
        draw.rectangle([(cell[1], cell[0]), (cell[1] + 1, cell[0] + 1)], fill=PATH_COLOR)

    # Save the image to a file
    img.save('maze_path.png')


if __name__ == '__main__':
    maze_file = 'maze-Easy.txt'
    maze = readMazeFile(maze_file)
    start, goal = find_start_and_goal(maze)
    path, nodes_explored, execution_time, visited = dfs(maze, start, goal)
    if path:
        visulizePath(maze, visited, path)
        print(f'Path found with {len(path)} steps in {execution_time:.4f} seconds.')
        print(f'Explored {nodes_explored} nodes.')
        for location in path:
            print(location)
    else:
        print('No path found.')
