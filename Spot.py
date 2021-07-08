import Color
import pygame

class Spot:
    def __init__(self, win, row, col, width, total_rows) -> None:
        self.win = win          # The window object from pygame
        
        self.row = row
        self.col = col
        self.x   = row * width  # X coordinate from top left of screen
        self.y   = col * width  # Y coordinate from top left of screen
        

        self.width = width
        self.total_rows = total_rows
        self.color = Color.WHITE        # Default spot color
        self.neighbors = []             # List of nearby Spot objects

        self.weight = 0

        self.closedColor = Color.RED
        self.openColor = Color.GREEN
        self.pathColor = Color.PURPLE
        self.barrierColor = Color.BLACK
        self.startColor = Color.ORANGE
        self.endColor = Color.TURQUOISE
        self.resetColor = Color.WHITE

        self.left = False
        self.right = False
        self.up = False
        self.down = False
   

    """
    Returns the row, col position as an unpackable tuple (row, col)
    """
    def getPosition(self):
        return self.row, self.col

    def isClosed(self):
        return self.color == self.closedColor

    def isOpen(self):
        return self.color == self.openColor

    def isPath(self):
        return self.color == self.pathColor

    def isBarrier(self):
        return self.color == self.barrierColor or self.weight != 0

    def isStart(self):
        return self.color == self.startColor

    def isEnd(self):
        return self.color == self.endColor

    def reset(self):
        self.color = self.resetColor
        self.weight = 0

    def makeOpen(self):
        self.color = self.openColor
    
    def makeClosed(self):
        self.color = self.closedColor

    def makeBarrier(self):
        self.color = self.barrierColor

    def makeStart(self):
        self.color = self.startColor

    def makeEnd(self):
        self.color = self.endColor

    def makePath(self, left=False, right=False, up=False, down=False):
        if not left and not right and not up and not down:
            self.color = self.pathColor
        else:
            self.left = left
            self.right = right
            self.up = up
            self.down = down
            self.color = self.resetColor


    """ Make the spot a particular color """
    def setColor(self, colortuple):
        self.color = colortuple

    """
    Draws the square on the screen at position (x,y) with width=height=self.width
    """
    def draw(self):
        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.width))

        # Draw the skinny path
        if self.left:
            pass
        if self.right:
            pass
        if self.up:
            pass
        if self.down:
            pass
        
    """
    Updates the square's neighbors field, so that the VALID neighbors are added.
    INVALID neighbors = out of bounds, or barriers
    """
    def updateNeighbors(self, grid):
        self.neighbors = []

        # Check Up
        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        
        # Check Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].isBarrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Check Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isBarrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Check Left
        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier():
            self.neighbors.append(grid[self.row][self.col - 1])


    """
    Less than function, 
    """
    def __lt__(self, other):
        return self.weight < other.weight

        

        

        

    


    


    
    
    
    
