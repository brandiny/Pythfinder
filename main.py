import pygame, os
import math
from Grid import Grid
from Spot import Spot
    

# Displays the window in center of page
os.environ['SDL_VIDEO_CENTERED'] = '1' 

# Program Constants
WIDTH  = 500
ROWS = 10
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

# Dynamic variables
start = None            # The start spot pointer
end = None              # The end spot pointer
run = True 
grid = Grid(WINDOW, ROWS, WIDTH)

# Handling the event function
def handleEvents():
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if pygame.mouse.get_pressed()[0]:
            spot = grid.getSpot(pygame.mouse.get_pos())
            spot.makeBarrier()


if __name__ == "__main__":
    while run:
        grid.draw()
        handleEvents()

       

        