import pygame
from display_constants import TITLE, TITLE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Title:

    def __init__ (self, surface, pos, size):
        """
        Title object.
        """
        self.img = TITLE
        self.surface = surface
        self.pos = pos
        self.x = pos[0] - TITLE.get_width() // 2 * TITLE_SIZE[0]
        self.y = pos[1] - TITLE.get_height() // 2 * TITLE_SIZE[1]
        self.w = size[0] * TITLE.get_width()
        self.h = size[1] * TITLE.get_height()

    def display(self):
        self.img = pygame.transform.smoothscale(TITLE, (self.w, self.h))
        self.surface.blit(self.img, (self.x, self.y))