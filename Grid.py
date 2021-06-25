import pygame
import Color
from Spot import Spot

class Grid:
    """
    Initialises a grid with a given amount of rows, and width in pixels across the screen
    """
    def __init__(self, win, rows, width):
        self.win = win
        self.grid = []
        self.gap  = width // rows
        self.rows = rows
        self.width = width
        
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
    Draws the grid on the pygame window
    """
    def draw(self):
        # Draws the grid lines
        for y in range(self.rows):
            pygame.draw.line(self.win, Color.GREY, (0, y * self.gap), (self.width, y * self.gap))
            for x in range(self.rows):
                pygame.draw.line(self.win, GREY, (x * self.gap, 0), (x * self.gap, self.width))

        # Draws the spots
        for row in self.grid:
            for spot in row:
                spot.draw()

        # Update - move to main eventually
        pygame.display.update()

    """
    Clear the green/red on the grid (algorithm working)
    """
    def clearWorking(self):
        for row in self.grid:
            for spot in row:
                if spot.color != Color.TURQUOISE and spot.color != Color.BLACK and spot.color != Color.ORANGE:
                    spot.color = Color.WHITE

    """
    Clear the start/end anchors
    """ 
    def clearStartEnd(self):
        for row in self.grid:
            for spot in row:
                if spot.color == Color.TURQUOISE or spot.color == Color.ORANGE:
                    spot.color = Color.WHITE