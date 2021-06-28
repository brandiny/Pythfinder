import pygame
import random
from Spot import Spot
"""
def randomDFSMaze(grid, start, end, draw):
    start = grid.grid[0][0]

    stack = []
    stack.append(start)

    visited = {start}
    parent = dict()

    last = Spot(grid.win, 0, -1, grid.width, grid.rows)
    slow = False
    while stack:
        for event in pygame.event.get():
            # Click on X
            if event.type == pygame.QUIT:
                run = False
        
        current = stack.pop()           # Grab the next spot in line to be processed

        if slow:
            pygame.time.wait(500)
            print(last.getPosition(), current.getPosition())
        # if current.getPosition() == (1, 4):
        #     slow = True

        # In the event it is not start or end - make it negative
        if current != start and current != end:
            visited.add(current)            # Make sure it is not visited again
            current.makeClosed()

        # Grab a random neighbor and add it to the next list
        n = random.choice(current.neighbors)
        if n not in visited:
            if n != end:
                n.makeOpen()
            stack.append(n)
            parent[n] = current
            


        
        xi, yi = last.getPosition()
        xf, yf = current.getPosition()
        
        # If not adjacent, skip
        if abs(xf - xi) > 1 or abs(yf - yi) > 1:
            pass
        
        # If you cross into the RIGHT, don't draw the left handside Y handle
        elif xf - xi == 1 and yf - yi == 0:
            grid.gridlines[yf][xf]["drawY"] = False

        # If you cross into the LEFT, don't draw the last right handside Y handle
        elif xf - xi == -1 and yf - yi == 0:
            grid.gridlines[yi][xi]["drawY"] = False

        # Down
        elif xf - xi == 0 and yf - yi == 1:
            grid.gridlines[yf][xf]["drawX"] = False

        # Up
        elif xf - xi == 0 and yf - yi == -1:
            grid.gridlines[yi][xi]["drawX"] = False
        
        last = current
        draw()
    
    grid.clearAll()
    draw()
"""

last = Spot(None, -1, 0, 1, 1)
def randomDFSMaze(grid, start, end, draw):
    start = grid.grid[0][0]
    randomDFS(start, grid, draw)
    grid.clearAll()

def randomUnvisitedNeighbor(spot):
    neighbors = [spot for spot in spot.neighbors if not spot.isClosed()]
    if not neighbors:
        return None
    else:
        return random.choice(neighbors)
    

def randomDFS(vertex, grid, draw):
    global last
    vertex.makeClosed()
    next = randomUnvisitedNeighbor(vertex)
    while next != None:
        randomDFS(next, grid, draw)
        next = randomUnvisitedNeighbor(vertex)

        xi, yi = last.getPosition()
        xf, yf = vertex.getPosition()
        
        # If not adjacent, skip
        if abs(xf - xi) > 1 or abs(yf - yi) > 1:
            pass
        
        # If you cross into the RIGHT, don't draw the left handside Y handle
        elif xf - xi == 1 and yf - yi == 0:
            grid.gridlines[yf][xf]["drawY"] = False

        # If you cross into the LEFT, don't draw the last right handside Y handle
        elif xf - xi == -1 and yf - yi == 0:
            grid.gridlines[yi][xi]["drawY"] = False

        # Down
        elif xf - xi == 0 and yf - yi == 1:
            grid.gridlines[yf][xf]["drawX"] = False

        # Up
        elif xf - xi == 0 and yf - yi == -1:
            grid.gridlines[yi][xi]["drawX"] = False
        
        last = vertex
        draw()

def getPath(start, end, parentDictionary):
    path = []
    pointer = end

    # Essentially traversing a linkedlist where head=end
    while pointer != start:         
        path.append(pointer)
        pointer = parentDictionary[pointer]

    return path[::-1]
