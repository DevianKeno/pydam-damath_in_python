import pygame
from ui_class.image import Image

class Window(Image):

    def __init__(self, img, surface, pos, size):
        self.source = img
        self.img = self.source
        self.surface = surface
        self.rect = img.get_rect()
        self.w = size[0]
        self.h = size[1]
        self.x = pos[0]
        self.y = pos[1]
        self.rotation = 0
        self.anim_scale = False
        self.anim_rot = False
        self.surface_center = (self.surface.get_width()//2, self.surface.get_height()//2)
        
        self.img = pygame.transform.smoothscale(self.source, (self.w, self.h))
        pass

    def display(self, pos):
        """
        Displays the image or updates if already displayed.
        """
        if self.anim_scale:
            self.img = pygame.transform.smoothscale(self.source, (self.w, self.h))
        if self.anim_rot:
            self.img = pygame.transform.rotozoom(self.source, self.rotation, 0.75)
            self.rotated_image_rect = self.img.get_rect(center = self.surface_center)
            self.surface.blit(self.img, self.rotated_image_rect)
            return
        
        self.x, self.y = pos
        self.surface.blit(self.img, (self.x, self.y))