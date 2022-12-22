import pygame

class Image:

    def __init__(self, img, surface, pos, size):
        """
        Tweenable image object.
        """
        self.source = img
        self.img = self.source
        self.surface = surface
        self.rect = img.get_rect()
        self.w = self.source.get_width() * size[0]
        self.h = self.source.get_height() * size[1]
        self.x = pos[0] - self.w // 2
        self.y = pos[1] - self.h // 2
        self.rotation = 0
        self.anim_scale = False
        self.anim_rot = False
        
        self.img = pygame.transform.smoothscale(self.source, (self.w, self.h))

    def display(self):
        """
        Displays the image or updates if already displayed.
        """
        if self.anim_rot:
            self.img = pygame.transform.rotate(self.source, self.rotation)
        if self.anim_scale:
            self.img = pygame.transform.smoothscale(self.source, (self.w, self.h))
        self.surface.blit(self.img, (self.x, self.y))