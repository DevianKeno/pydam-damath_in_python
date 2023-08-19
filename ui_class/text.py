import pygame
from ui_class.font import *

class Text:
    
    def __init__(self, surface, font, font_size, color, align='center') -> None:
        self.surface = surface
        self.font = font
        self.font_size = font_size
        self.color = color
        self.align = align
        self.IsActive = True
        
        self.text = ''
        self.pos = (0, 0)
        self.rect = None
        
        self._font = pygame.font.Font(font, int(font_size))

        self.text_surface = self._font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()
        self.surface.blit(self.text_surface, self.rect)

    def draw(self):
        if not self.IsActive:
            return

        self.text_surface = self._font.render(self.text, True, self.color)
        
        if self.align == 'center':
            self.rect = self.text_surface.get_rect(center=self.pos)
        else:
            self.rect = self.text_surface.get_rect(topleft=self.pos)

        self.surface.blit(self.text_surface, self.rect)

    def update(self):
        """
        Call this function whenever the font and/or font size is changed.
        """
        self._font = pygame.font.Font(self.font, int(self.font_size))

    def change_color(self, color):
        self.color = color

    def hover(self):
        pass