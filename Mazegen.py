import pygame
import random
from Spot import Spot

"""
Given a spot, return a random neighbor from its neighbors. If no possible options none
"""
def randomUnvisitedNeighbor(spot) -> Spot:
    neighbors = [spot for spot in spot.neighbors if not spot.isClosed()]
    if not neighbors:
        return None
    else:
        return random.choice(neighbors)

"""
Generates a random maze given a grid object
"""
def DFSMaze(grid, start, end, draw):
    grid.fillGridLines()
    start = grid.grid[0][0]
    last = Spot(None, -1, 0, 1, 1)
    
    stack = [start]
    while stack:
        vertex = stack[-1]
        vertex.makeClosed()
        next = randomUnvisitedNeighbor(vertex)
        # If no more neighbors, end this vertex
        if next == None:
            stack.pop()
        else:
            stack.append(next)

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
        pygame.display.update()
    
    grid.clearWorking()

  
def BTMaze(grid, start, end, draw):
    grid.fillGridLines()
    for y in range(grid.rows):
        for x in range(grid.rows):

            if x == 0 and y == 0:
                carveWest = True
                carveNorth = True

            elif x == 0:
                carveWest = True
                carveNorth = False

            elif y == 0:
                carveNorth = True
                carveWest = False
            
            else:
                carveWest = random.choice([True, False])
                carveNorth = not carveWest

            grid.gridlines[y][x]["drawY"] = carveWest
            grid.gridlines[y][x]["drawX"] = carveNorth
            
            if not grid.grid[x][y].isStart() and not grid.grid[x][y].isEnd():
                grid.grid[x][y].makeClosed()

            draw()
            pygame.display.update()

    grid.clearWorking()
     


def getPath(start, end, parentDictionary):
    path = []
    pointer = end

    # Essentially traversing a linkedlist where head=end
    while pointer != start:         
        path.append(pointer)
        pointer = parentDictionary[pointer]

    return path[::-1]
