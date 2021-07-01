import pygame, os
import math

import Pathfind
import Mazegen
from Grid import Grid
from Spot import Spot
from Controls import Controls

# Fires up pygame
pygame.init() 

# Displays the window in center of page
os.environ['SDL_VIDEO_CENTERED'] = '1' 

# Program Constants
CONTROL_PANEL_HEIGHT = 140
WIDTH  = 500
ROWS =  25
WINDOW = pygame.display.set_mode((WIDTH, WIDTH + CONTROL_PANEL_HEIGHT))

# Dynamic variables
run = True                          # Exit boolean for program
grid = Grid(WINDOW, ROWS, WIDTH)    # Grid object that renders to the screeen
controls = Controls(                # Control panel object that renders to the screen
    WINDOW,
    grid,
    WIDTH,
    CONTROL_PANEL_HEIGHT
)

# Handling the event function
def handleEvents():
    global run

    for event in pygame.event.get():
        # Click on X
        if event.type == pygame.QUIT:
            run = False
            
        # LMB
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            
            # If clicking within the bounds of the grid
            if x < WIDTH and y < WIDTH:
                spot = grid.getSpot(pygame.mouse.get_pos())

                if not grid.start and spot != grid.end:
                    grid.makeStart(spot)

                elif not grid.end and spot != grid.start:
                    grid.makeEnd(spot)

                elif spot != grid.end and spot != grid.start:
                    grid.makeBarrier(spot)
            
            # Otherwise the click lands within the control region
            controls.handleClick(x, y)

        # RMB
        if pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()
            
            # If clicking within the bounds of the grid
            if x < WIDTH and y < WIDTH:
                spot = grid.getSpot(pygame.mouse.get_pos())
                grid.start = None if spot == grid.start else grid.start
                grid.end = None if spot == grid.end else grid.end
                spot.reset()

        # Key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                grid.makeMaze()

            if event.key == pygame.K_SPACE:
                grid.findPath()

                
if __name__ == "__main__":
    while run:
        grid.draw()
        controls.draw()
        handleEvents()
        pygame.display.update()

       

        