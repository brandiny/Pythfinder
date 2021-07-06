import pygame
import Color
import Pathfind
import Mazegen
from Spot import Spot

class Grid:
    """
    Initialises a grid with a given amount of rows, and width in pixels across the screen
    """
    def __init__(self, win, rows, width):
        self.win = win
        self.gap  = width // rows
        self.rows = rows
        self.width = width

        self.start = None
        self.end = None

        self.grid = []
        self.fillGrid()

        self.gridlines = []
        self.fillGridLines()
        
        self.pathfindFunction = Pathfind.breadthFirstSearch
        self.mazegenFunction = Mazegen.BTMaze

        self.drawWeighted = False

    """
    Remake the self.gridlines
    """ 
    def fillGridLines(self):
        self.gridlines = []
        for r in range(self.rows):
            row = []
            for c in range(self.rows):
                row.append({"drawY" : True, "drawX" : True})
            self.gridlines.append(row)

        
    """
    Remake the self.grid
    """
    def fillGrid(self):
        self.grid = []
        for r in range(self.rows):
            row = []
            for c in range(self.rows):
                row.append(Spot(self.win, r, c, self.gap, self.rows))
            self.grid.append(row)

    """
    Update neighbors on the grid
    """
    def updateSpotNeighbors(self):
        for row in self.grid:
            for spot in row:
                spot.updateNeighbors(self.grid)

    """
    Draws the grid on the pygame window
    """
    def draw(self):
        # Draws the spots
        for row in self.grid:
            for spot in row:
                spot.draw()
                
        # Draws the gridlines over top
        for y in range(self.rows):
            for x in range(self.rows):  
                if self.gridlines[y][x]["drawX"]:
                    pygame.draw.line(self.win, Color.GREY, (x * self.gap, y * self.gap), ((x + 1) * self.gap, y * self.gap))
                if self.gridlines[y][x]["drawY"]:
                    pygame.draw.line(self.win, Color.GREY, (x * self.gap, y * self.gap), (x * self.gap, (y + 1) * self.gap))

       
        

    """
    Clear the green/red on the grid (algorithm working)
    """
    def clearWorking(self):
        for row in self.grid:
            for spot in row:
                if spot.color == Color.GREEN or spot.color == Color.RED or spot.color == Color.PURPLE:
                    spot.reset()

    """
    Clear the start/end anchors
    """ 
    def clearStartEnd(self):
        for row in self.grid:
            for spot in row:
                if spot.color == Color.TURQUOISE or spot.color == Color.ORANGE:
                    spot.reset()

    """
    Clear maze
    """
    def clearMaze(self):
        self.fillGridLines()

    """
    Clears all spots --> white
    """
    def clearAll(self):
        self.end, self.start = None, None
        for row in self.grid:
            for spot in row:
                spot.reset();

        self.clearMaze()

    """
    Clears all barriers
    """
    def clearBarriers(self):
        for row in self.grid:
            for spot in row:
                if spot.isBarrier():
                    spot.reset()
    """
    Clears all mazeLines --> white
    """
    def clearAllMaze(self):
        self.fillGridLines
        

    """
    Returns the R, C --> given X, Y
    """
    def getClickPosition(self, xytuple, rows, width):
        gap = width // rows
        y, x = xytuple
        row = y // gap
        col = x // gap
        return row, col

    """
    Get the spot at this x/y position
    """
    def getSpot(self, xytuple):
        row, col = self.getClickPosition(xytuple, self.rows, self.width)
        return self.grid[row][col]

    """
    Prints the efficiency of the algorithm (searched spaces vs path)
    """
    def printEfficiency(self):
        totalRed = 0
        totalPath = 0
        for r in self.grid:
            for spot in r:
                if spot.isClosed():
                    totalRed += 1
                elif spot.isPath():
                    totalPath += 1
        
        print("Efficiency: " + str(round(100 * totalPath / (totalRed + totalPath))) + "%")
    
    """
    Runs the path finding function, after clearing working
    """
    def findPath(self):
        self.clearWorking()
        self.updateSpotNeighbors()
        self.pathfindFunction(self, self.start, self.end, lambda : self.draw())

    def makeMaze(self):
        self.clearWorking()
        self.updateSpotNeighbors()
        self.mazegenFunction(self, self.start, self.end, lambda : self.draw())
    
    def makeStart(self, spot):
        spot.makeStart()
        self.start = spot

    def makeEnd(self, spot):
        spot.makeEnd()
        self.end = spot

    def setPathfindFunction(self, func):
        self.pathfindFunction = func
        self.findPath()

    def setMazegenFunction(self, func):
        self.mazegenFunction = func
        self.makeMaze()
    
    def toggleDrawWeighted(self):
        self.drawWeighted = not self.drawWeighted

    def makeBarrier(self, spot):
        if self.drawWeighted:
            spot.weight += 1
            weight = spot.weight
            r, g, b = 255, 255, 255
            r, g, b = max(0, r - weight*20), max(0, g - weight*20), max(0, b - weight*20)
            spot.setColor((r, g, b))
        else:
            spot.makeBarrier()
