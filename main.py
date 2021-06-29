import pygame, os
import math

import Pathfind
import Mazegen
from Grid import Grid
from Spot import Spot
    

# Displays the window in center of page
os.environ['SDL_VIDEO_CENTERED'] = '1' 

# Program Constants
WIDTH  = 500
ROWS =  25
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

# Dynamic variables
start = None            # The start spot pointer
end = None              # The end spot pointer
run = True 
grid = Grid(WINDOW, ROWS, WIDTH)

# Handling the event function
def handleEvents():
    global run
    global start
    global end

    for event in pygame.event.get():
        # Click on X
        if event.type == pygame.QUIT:
            run = False
            
        # LMB
        if pygame.mouse.get_pressed()[0]:
            spot = grid.getSpot(pygame.mouse.get_pos())
            
            if not start and spot != end:
                start = spot
                start.makeStart()

            elif not end and spot != start:
                end = spot
                end.makeEnd()

            elif spot != end and spot != start:
                spot.weight += 1
                weight = spot.weight
                r, g, b = 255, 255, 255
                r, g, b = max(0, r - weight*20), max(0, g - weight*20), max(0, b - weight*20)

                # spot.setColor((r, g, b))
                spot.makeBarrier()

        # RMB
        if pygame.mouse.get_pressed()[2]:
            spot = grid.getSpot(pygame.mouse.get_pos())
            spot.reset()

            start = None if spot == start else start
            end = None if spot == end else end

        # 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                grid.clearWorking()
                grid.updateSpotNeighbors()
                # Pathfind.aStarSearch(grid, start, end, lambda : grid.draw())
                Mazegen.randomDFSMaze(grid, start, end, lambda : grid.draw());
                Pathfind.solveMazeBFS(grid, start, end, lambda : grid.draw());
                # grid.printEfficiency()

                
if __name__ == "__main__":
    while run:
        grid.draw()
        handleEvents()


       

        