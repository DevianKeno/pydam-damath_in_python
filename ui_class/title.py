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
        self.w = size[0]
        self.h = size[1]
        self.x = pos[0] - self.w // 2
        self.y = pos[1] - self.h // 2
        self.rotation = 0
        self.anim_scale = False
        self.anim_rot = False
        self.surface_center = (self.surface.get_width()//2, self.surface.get_height()//2)
        
        self.img = pygame.transform.smoothscale(self.source, (self.w, self.h))

    def display(self):
        """
        Displays the image or updates if already displayed.
        """
        
        # self.rotated_image_rect = self.img.get_rect(center = self.surface_center)
        # if self.anim_rot:
        #     self.img = pygame.transform.rotate(self.source, self.rotation)
        #     self.rotated_image_rect = self.img.get_rect(center = self.surface_center)
        # if self.anim_scale:
        #     self.img = pygame.transform.smoothscale(self.source, (self.w, self.h))
        self.surface.blit(self.img, (self.x, self.y))