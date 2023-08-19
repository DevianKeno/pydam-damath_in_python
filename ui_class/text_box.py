import pygame
from ui_class.colors import BLACK

class TextBox:

    def __init__(self, surface, input, rect=None, text='') -> None:
        self.surface = surface
        self.input = input
        # self.color = color
        self.rect = rect
        self.IsActive = True
        self.x = rect.x
        self.y = rect.y
        self.text = text

    def draw(self):
        if not self.IsActive:
            return
            
        self.text = self.input.text

        self.text_surface = self.input._font.render(self.text, True, self.input.color)
        text_rect = self.text_surface.get_rect(center=(self.rect.center))
        self.surface.blit(self.text_surface, text_rect)

    def update(self):
        self.text_surface = self.input._font.render(self.text, True, self.input.color)

    def clear(self):
        self.input.text = ''