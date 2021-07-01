import pygame
import Color
import Pathfind
import Mazegen
from Button import Button


class Controls:
    """
    Initialises a control panel with widthxheight, beginning from (0, width)
    """
    def __init__(self, win, grid, width, height) -> None:
        self.win = win
        self.grid = grid
        self.width = width
        self.height = height
        self.rows = 4
        self.columns = 4 
        self.widthGap = width / self.columns
        self.heightGap = height / self.rows
        self.buttons = []
        self.createGUI()


    def drawBackground(self) -> None:
        pygame.draw.rect(self.win, Color.RED, (0, self.width, self.width, self.height))


    def drawButtons(self) -> None:
        for b in self.buttons:
            b.draw()
            

    def draw(self) -> None:
        self.drawBackground()
        self.drawButtons()


    def addButton(self, row, col, text, color, function) -> None:
        x = self.widthGap * row
        y = self.heightGap * col
        self.buttons.append(
            Button(self.win, self.width, x, y, self.widthGap, self.heightGap, text, color, function)
        )

    """
    Creates the GUI, fills up self.buttons
    """
    def createGUI(self) -> None:
        self.addButton(0, 0, "Clear working", Color.YELLOW, lambda : self.grid.clearWorking())
        self.addButton(0, 1, "Clear barriers", Color.GREEN, lambda : self.grid.clearBarriers())
        self.addButton(0, 2, "Clear maze", Color.YELLOW, lambda : self.grid.clearMaze())
        self.addButton(0, 3, "Clear all", Color.YELLOW, lambda : self.grid.clearAll())
        self.addButton(1, 0, "Use BFS", Color.YELLOW, lambda : self.grid.setPathfindFunction(Pathfind.breadthFirstSearch))
        self.addButton(1, 1, "Use DFS", Color.GREEN, lambda : self.grid.setPathfindFunction(Pathfind.depthFirstSearch))
        self.addButton(1, 2, "Use A* search", Color.YELLOW, lambda : self.grid.setPathfindFunction(Pathfind.aStarSearch))
        self.addButton(1, 3, "Dijkstra's", Color.YELLOW, lambda : self.grid.setPathfindFunction(Pathfind.dijkstraSearch))
        self.addButton(2, 0, "BT maze", Color.GREEN, lambda : self.grid.setMazegenFunction(Mazegen.BTMaze))
        self.addButton(2, 1, "DFS maze", Color.GREEN, lambda : self.grid.setMazegenFunction(Mazegen.DFSMaze))
        self.addButton(3, 0, "Toggle draw", Color.GREEN, lambda : self.grid.toggleDrawWeighted())

    """
    Given an x, y position, if this x, y lands within a button, trigger that buttons function
    """
    def handleClick(self, x, y):
        for b in self.buttons:
            if x >= b.x and y >= b.y and x <= b.x + b.width and y <= b.y + b.height:
                b.trigger()
            
