import pygame
import Color

class Label:
    def __init__(self, win, offset, x, y, width, height, text, color) -> None:
        self.win = win
        self.x = x
        self.y = y + offset
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.offset = offset
        self.fontsize = 22
        self.font = pygame.font.SysFont(None, self.fontsize)
        self.darken = False

    def draw(self) -> None:
        if self.font != None:
            pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
            self.win.blit(self.font.render(self.text, True, Color.BLACK), (self.x + self.fontsize / 2, self.y + self.height / 2 - self.fontsize / 4))


