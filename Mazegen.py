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
    grid.updateSpotNeighbors()
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
     

def sidewinderMaze(grid, start, end, draw):
    grid.fillGridLines()

    # Carve out top passage
    for i in range(1, len(grid.gridlines[0])):
        grid.gridlines[0][i]["drawY"] = False

    for i in range(1, len(grid.gridlines)):
        run = set()
        for j in range(len(grid.gridlines[i])):
            
            run.add((i, j))
            grid.grid[j][i].makeOpen()
            carveEast = random.choice([True, False])

            draw()
            pygame.display.update()

            if carveEast:
                if j != len(grid.gridlines[i]) - 1:
                    grid.gridlines[i][j+1]["drawY"] = False
                else:
                    grid.gridlines[i][j]["drawX"] = False
                    i, j = random.choice(list(run))
                    for tup in list(run):
                        row, col = tup
                        grid.grid[col][row].reset()

            else:
                i, j = random.choice(list(run))
                for tup in list(run):
                    row, col = tup
                    grid.grid[col][row].reset()

                grid.gridlines[i][j]["drawX"] = False
                run.clear()
            
            
            
def primsAlgorithmMaze(grid, start, end, draw):
    grid.fillGridLines()
    grid.updateSpotNeighbors()
    
    # Stores the edge of the maze variables - starts with random variable
    initial = grid.grid[random.randint(0, len(grid.grid) - 1)][random.randint(0, len(grid.grid) - 1)]
    frontier = [initial]
    
    # When this is full we done
    visited = set([initial])

    # In maze
    maze = set()

    while frontier:
        # Choose random frontier value
        current = random.choice(frontier)
        current.makeClosed()

        frontier.remove(current)
        maze.add(current)

        # Add neighbors to frontier
        random.shuffle(current.neighbors)
        for n in current.neighbors:
            if n not in visited:
                connectCells(grid, current, n)
                frontier.append(n)
                n.makeOpen()
                visited.add(n)
    
        # Redraw the graphics pane
        draw()
        pygame.display.update()
    

    # Clear all of the working
    grid.clearWorking()
    draw()
    pygame.display.update()

def connectCells(grid, cell1, cell2):
    x1, y1 = cell1.getPosition()
    x2, y2 = cell2.getPosition()

    if x2 - x1 == 1 and y2 - y1 == 0: # Right
        grid.gridlines[y2][x2]["drawY"] = False
        
    elif x2 - x1 == -1 and y2 - y1 == 0: # Left
        grid.gridlines[y1][x1]["drawY"] = False
        
    elif x2 - x1 == 0 and y2 - y1 == 1: # Down
        grid.gridlines[y2][x2]["drawX"] = False
        
    elif x2 - x1 == 0 and y2 - y1 == -1: #Up
        grid.gridlines[y1][x1]["drawX"] = False
        


def getPath(start, end, parentDictionary):
    path = []
    pointer = end

    # Essentially traversing a linkedlist where head=end
    while pointer != start:         
        path.append(pointer)
        pointer = parentDictionary[pointer]

    return path[::-1]
