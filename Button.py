import pygame
import Color

class Button:
    def __init__(self, win, offset, x, y, width, height, text, color, function) -> None:
        self.win = win
        self.x = x
        self.y = y + offset
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.function = function
        self.offset = offset
        self.fontsize = 22
        self.font = pygame.font.SysFont(None, self.fontsize)
        self.darken = False

    def draw(self) -> None:
        if self.font != None:
            pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
            self.win.blit(self.font.render(self.text, True, Color.BLACK), (self.x + self.fontsize / 2, self.y + self.height / 2 - self.fontsize / 4))
            
    def trigger(self) -> None:
        # Delay of the button going back up in milliseconds
        delay = 90

        self.darkenColor()
        self.draw()
        pygame.display.update()
        pygame.time.wait(delay)
        
        self.darkenColor()
        self.draw()
        
        self.function()

    def darkenColor(self) -> None:
        self.scale = 1.4
        if self.darken == False:
            r, g, b = self.color
            r /= 1.4
            g /= 1.4
            b /= 1.4
            self.color = (r, g, b)
            self.darken = True
        else:
            r, g, b = self.color
            r *= 1.4
            g *= 1.4
            b *= 1.4
            self.color = (r, g, b)
            self.darken = False
