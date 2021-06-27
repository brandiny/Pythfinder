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

    """
    Returns the row, col position as an unpackable tuple (row, col)
    """
    def getPosition(self):
        return self.row, self.col

    """ Is the spot visited? """
    def isClosed(self):
        return self.color == Color.RED

    """ Is the spot unvisited? """
    def isOpen(self):
        return self.color == Color.GREEN
    
    """ Is the spot a barrier? """
    def isBarrier(self):
        return self.color == Color.BLACK

    """ Is the spot the start? """
    def isStart(self):
        return self.color == Color.ORANGE

    """ Is the spot unvisited? """
    def isEnd(self):
        return self.color == Color.TURQUOISE

    """ Reset the square to white? """
    def reset(self):
        self.color = Color.WHITE

    """ Make the spot to be visited """
    def makeOpen(self):
        self.color = Color.GREEN

    """ Make the spot to be visited """
    def makeBarrier(self):
        self.color = Color.BLACK

    """ Make the spot to be start """
    def makeStart(self):
        self.color = Color.ORANGE

    """ Make the spot to be end """
    def makeEnd(self):
        self.color = Color.TURQUOISE

    """ Make the spot to be final path """
    def makePath(self):
        self.color = Color.PURPLE

    """
    Draws the square on the screen at position (x,y) with width=height=self.width
    """
    def draw(self):
        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.width))
        

    """
    Updates the square's neighbors field, so that the VALID neighbors are added.
    INVALID neighbors = out of bounds, or barriers
    """
    def updateNeighbors(self, grid):
        self.neighbors = []

        # Check Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isBarrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Check Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Check Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Check Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    


    


    
    
    
    
