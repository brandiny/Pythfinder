import pygame
import heapq
from queue import PriorityQueue
from collections import deque
import Color

"""PATH FINDING ALGORITHMS SECTION"""


"""
Finds the shortest path using BFS and paints the path

grid --> Grid object
start --> Spot object
end --> Spot object
draw --> draw() function object
"""
def breadthFirstSearch(grid, start, end, draw):
    isMaze = checkMaze(grid)            # Check if is maze
    if start == None or end == None:    # Makes sure you can't accidentally call it
        return
    
    queue = deque([])                   # Processes nodes in a FIFO manner
    queue.append(start)     

    visited = set()                     # Only process !visited nodes
    parent = dict()                     # parent[node] = where the node came from

    while queue:
        current = queue.popleft()       # Grab the next spot in line to be processed
        visited.add(current)            # Mark as visited
        
        # In the event it is not start or end - make closed (nothing is there)
        if current != start and current != end:
            current.makeClosed()

        # If it is the end, then draw the path and break out.
        elif current == end:
            path = getPath(start, end, parent)
            for p in path:
                p.makePath()
            end.makeEnd()
            start.makeStart()
            return
            
        # Then, add all valid neighbors (unvisited ones) to the queue to be processed.
        # Notice we add them to visited, so that the BFS algorithm doesn't overlap
        for n in current.neighbors:
                if isMaze:
                    if n not in visited and not hitsWall(grid, current, n):
                        if n != end:
                            n.makeOpen()
                        queue.append(n)
                        visited.add(n)          
                        parent[n] = current
                else:
                    if n not in visited:
                        if n != end:
                            n.makeOpen()
                        queue.append(n)
                        visited.add(n)          
                        parent[n] = current
        
        # Redraw - comment out for performance - uncomment for interactive
        draw()
        pygame.display.update()
    

"""
Finds a possible path (does not guarantee shortest path) with DFS

grid --> Grid object
start --> Spot object
end --> Spot object
draw --> draw() function object
"""
def depthFirstSearch(grid, start, end, draw):
    isMaze = checkMaze(grid)            # Check if is maze
    if start == None or end == None:    # Makes sure you can't accidentally call it
        return

    stack = []                          # Processes nodes in a LIFO manner so that its depth first
    stack.append(start) 

    visited = set()                     # Tracks with nodes have been visited           
    parent = dict()                     # parent[spot] = which spot this came from

    while stack:
        # Grab the next spot in line to be processed
        # Make sure its never visited again
        current = stack.pop()           
        visited.add(current)            

        # If it isn't what we are looking for, mark it as closed
        if current != start and current != end:
            current.makeClosed()
        
        # If we find the end, we reconstruct the path and exit.
        elif current == end:
            path = getPath(start, end, parent)
            for p in path:
                p.makePath()
            end.makeEnd()
            start.makeStart()
            return
    
        # Otherwise, we add all valid, unvisited neighbors to the stack
        for n in current.neighbors:
            if isMaze:
                if n not in visited and not hitsWall(grid, current, n):
                    if n != end:
                        n.makeOpen()
                    stack.append(n)
                    parent[n] = current
            else:
                if n not in visited:
                    if n != end:
                        n.makeOpen()
                    stack.append(n)
                    parent[n] = current
    
        # Comment for performance - live drawing function
        draw()
        pygame.display.update()
    


"""
Finds a the shortest path with A*

grid --> Grid object
start --> Spot object
end --> Spot object
draw --> draw() function object
"""
def aStarSearch(grid, start, end, draw):
    isMaze = checkMaze(grid)            # Check if is maze
    if start == None or end == None:    # Makes sure you can't accidentally call it
        return
    
    count = 0                           # Used for breaking ties where F score is    
    openSet = PriorityQueue()           # Priority Queue based on first element of tuple
    openSet.put((0, count, start))      # (FScore, Tiebreak_count, spot object)
    parent = {}                         # parent[spot] = where spot came from (returns spot)

    # G Score = the SHORTEST known distance to arrive at given spot from start
    # gScore[start] = 0, as it is already at start
    # Initialise all other G Scores at infinity because we don't know the path yet
    gScore = {spot: float('inf') for row in grid.grid for spot in row}
    gScore[start] = 0

    # F Score = G Score + H Score
    # H Score = 'estimated' distance to the end node from the current node with heuristic
    # Therefore F score is total cost to arrive at end.
    fScore = {spot: float('inf') for row in grid.grid for spot in row}
    fScore[start] = hScore(start.getPosition(), end.getPosition())

    visited = {start}                   # Tracks whether spots have been visited    
   
    while not openSet.empty():
        current = openSet.get()[2]
        # visited.remove(current)

        # If it is not equal to the end, we make it closed
        if current != start and current != end:
            current.makeClosed()

        # If we find the end, reconstruct the path and exit
        elif current == end:
            path = getPath(start, end, parent)
            for p in path:
                p.makePath()
                draw()
                pygame.display.update()
            end.makeEnd()
            start.makeStart()
            return

        # Otherwise, for each neighbor
        for n in current.neighbors:
            if isMaze and hitsWall(grid, current, n):
                continue

            # If the temp gScore (distance to this node from root from this path)
            # is better than the best, update it and its F score
            # Otherwise do nothing to this neighbor.
            # Make sure it is unvisited too
            gScoreTemp = gScore[current] + 1
            if (gScoreTemp < gScore[n]):
                parent[n] = current
                gScore[n] = gScoreTemp
                fScore[n] = gScoreTemp + hScore(n.getPosition(), end.getPosition())
                if n not in visited:
                    count += 1
                    openSet.put((fScore[n], count, n))
                    visited.add(n)
                    n.makeOpen()

        # Live drawing, uncomment for better performance
        draw()
        pygame.display.update()
    


def dijkstraSearch(grid, start, end, draw):
    dist = {spot: float('inf') for row in grid.grid for spot in row}
    dist[start] = 0

    parent = dict()
    visited = set([start])

    queue = [(dist[spot], spot) for row in grid.grid for spot in row]
    heapq.heapify(queue)

    while len(queue):
        current = heapq.heappop(queue)[1]
        visited.add(current)

        # If it is not equal to the end, we make it closed
        if current != start and current != end:
            current.makeClosed()

        for n in current.neighbors:
            if n not in visited:
                distance_to = dist[current] + n.weight
                if distance_to < dist[n]:
                    parent[n] = current
                    dist[n] = distance_to
                    if n.color == Color.WHITE:
                        n.makeOpen()
                    
        while len(queue):
            heapq.heappop(queue)
            
        queue = [(dist[spot], spot) for row in grid.grid for spot in row if spot not in visited]
        heapq.heapify(queue)
            
        # Live drawing, uncomment for better performance
        draw()
        pygame.display.update()

    path = getPath(start, end, parent)
    for p in path:
        p.makePath()
        draw()
        pygame.display.update()
    end.makeEnd()
    start.makeStart()
    return

def greedyBestFirstSearch(grid, start, end, draw):
    isMaze = checkMaze(grid)            # Check if is maze
    if start == None or end == None:    # Makes sure you can't accidentally call it
        return
    
    queue = PriorityQueue()                   # Processes nodes in a FIFO manner
    queue.put((0, start))     

    visited = set()                     # Only process !visited nodes
    parent = dict()                     # parent[node] = where the node came from

    while not queue.empty():
        current = queue.get()[1]       # Grab the next spot in line to be processed
        visited.add(current)            # Mark as visited
        
        # In the event it is not start or end - make closed (nothing is there)
        if current != start and current != end:
            current.makeClosed()

        # If it is the end, then draw the path and break out.
        elif current == end:
            path = getPath(start, end, parent)
            for p in path:
                p.makePath()
            end.makeEnd()
            start.makeStart()
            return
            
        # Then, add all valid neighbors (unvisited ones) to the queue to be processed.
        # Notice we add them to visited, so that the BFS algorithm doesn't overlap
        for n in current.neighbors:
                if isMaze:
                    if n not in visited and not hitsWall(grid, current, n):
                        if n != end:
                            n.makeOpen()
                        queue.put((hScore(n.getPosition(), end.getPosition()), n))
                        visited.add(n)          
                        parent[n] = current
                else:
                    if n not in visited:
                        if n != end:
                            n.makeOpen()
                        queue.put((hScore(n.getPosition(), end.getPosition()), n))
                        visited.add(n)          
                        parent[n] = current
        
        # Redraw - comment out for performance - uncomment for interactive
        draw()
        pygame.display.update()


""" HELPER SUPPORT FUNCTIONS BELOW """


"""
Returns a list of the path from start to finish

start: starting Spot node
end: ending Spot node
parentDictionary: linked list of where each node came from
"""
def getPath(start, end, parentDictionary) -> list:
    path = []
    pointer = end 

    # Essentially traversing a linkedlist where head=end
    while pointer != start:         
        path.append(pointer)
        pointer = parentDictionary[pointer]
    
    # List is reversed because we add it in reverse order.
    print("Path length: ", len(path))
    return path[::-1] 
    

"""
Returns the estimated distance between two points via euclidean d

start: starting Spot node
end: ending Spot node
parentDictionary: linked list of where each node came from
"""
def hScore(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)


"""
Returns whether or not initial -> final is between a wall.

grid: Grid object
initial: Spot object
final: Spot object
"""
def hitsWall(grid, initial, final) -> bool:
    xi, yi = initial.getPosition()
    xf, yf = final.getPosition()

    # If you cross into the RIGHT, don't draw the left handside Y handle
    if xf - xi == 1 and yf - yi == 0 and grid.gridlines[yf][xf]["drawY"]:
        return True

    # If you cross into the LEFT, don't draw the last right handside Y handle
    elif xf - xi == -1 and yf - yi == 0 and grid.gridlines[yi][xi]["drawY"]:
        return True

    # Down
    elif xf - xi == 0 and yf - yi == 1 and grid.gridlines[yf][xf]["drawX"]:
        return True

    # Up
    elif xf - xi == 0 and yf - yi == -1 and grid.gridlines[yi][xi]["drawX"]:
        return True
    
    else:
        return False


def checkMaze(grid):
    for row in grid.gridlines:
        for tile in row:
            if tile["drawX"] == False or tile["drawY"] == False:
                return True
    
    return False

    

        

        
