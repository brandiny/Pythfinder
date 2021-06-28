import pygame
import Color
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
        self.grid = []
        self.fillGrid()
        self.gridlines = []
        self.fillGridLines()
        
    """
    Remake the self.gridlines
    """ 
    def fillGridLines(self):
        for r in range(self.rows):
            row = []
            for c in range(self.rows):
                row.append({"drawY" : True, "drawX" : True})
            self.gridlines.append(row)

        
    """
    Remake the self.grid
    """
    def fillGrid(self):
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
                
                
        # Draws the grid lines
        # for y in range(self.rows):
        #     pygame.draw.line(self.win, Color.GREY, (0, y * self.gap), (self.width, y * self.gap))
        #     for x in range(self.rows):
        #         pygame.draw.line(self.win, Color.GREY, (x * self.gap, 0), (x * self.gap, self.width))

        for y in range(self.rows):
            for x in range(self.rows):  
                if self.gridlines[y][x]["drawX"]:
                    pygame.draw.line(self.win, Color.GREY, (x * self.gap, y * self.gap), ((x + 1) * self.gap, y * self.gap))
                if self.gridlines[y][x]["drawY"]:
                    pygame.draw.line(self.win, Color.GREY, (x * self.gap, y * self.gap), (x * self.gap, (y + 1) * self.gap))

       

        # Update - move to main eventually
        pygame.display.update()

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
    Clears all spots --> white
    """
    def clearAll(self):
        for row in self.grid:
            for spot in row:
                spot.reset();

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

    