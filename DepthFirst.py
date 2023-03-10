import time
from collections import deque


def readMazeFile(fileName):
    """Reads in a maze file and returns a 2D list representing the maze."""
    mazeArray = []
    with open(fileName, 'r') as f:
        for line in f:
            mazeArray.append(list(line.strip().split()))
    return mazeArray


def findStartAndGoal(maze):
    """Finds the start and goal nodes in the maze."""
    try:
        startPoint = (0, maze[0].index("-"))
        goalPoint = (len(maze) - 1, maze[-1].index("-"))
        return startPoint, goalPoint
    except:
        print("Invalid Maze File")


def isValidLocation(maze, location):
    """Checks if a location is a valid path in the maze.
    """
    row, col = location
    if row < 0 or row >= len(maze) or col < 0 or col >= len(maze[0]):
        return False
    if maze[row][col] == '#':
        return False
    return True


def getValidNeighbors(maze, location):
    """Returns a list of valid neighboring locations."""
    row, col = location
    neighbors = [(row - 1, col), (row, col + 1), (row + 1, col), (row, col - 1)]
    validNeighbors = [neighbor for neighbor in neighbors if isValidLocation(maze, neighbor)]
    return validNeighbors


def bfs(maze, start, goal):
    """Performs breadth-first search on the maze."""
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
            return path, nodesExplored, endTime - startTime

        for neighbor in getValidNeighbors(maze, current):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    # We didn't find the goal node.
    return None, nodesExplored, time.time() - startTime


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
            return path, nodesExplored, endTime - startTime

        for neighbor in getValidNeighbors(maze, current):
            if neighbor not in visited:
                stack.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    # We didn't find the goal node.
    return None, nodesExplored, time.time() - startTime


if __name__ == '__main__':
    maze_file = 'maze-VLarge.txt'
    maze = readMazeFile(maze_file)
    start, goal = findStartAndGoal(maze)
    parent = {}
    path, nodes_explored, execution_time = dfs(maze, start, goal)
    if path:
        print(f'Path found with {len(path)} steps in {execution_time:.4f} seconds.')
        print(f'Explored {nodes_explored} nodes.')
        for location in path:
            print(location)
    else:
        print('No path found.')
