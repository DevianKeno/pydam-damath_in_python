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
        self.pos = pos
        self.x = pos[0] - self.w // 2
        self.y = pos[1] - self.h // 2
        self.pos_center = pos
        self.rotation = 0
        self.anim_scale = False
        self.anim_rot = False
        self.surface_center = (self.surface.get_width()//2, self.surface.get_height()//2)
        
        self.img = pygame.transform.smoothscale(self.source, (self.w, self.h))
        self.init_alpha = 255

    def reset_alpha(self):
        self.init_alpha = 255

    def display(self, alpha=255):
        """
        Displays the image or updates if already displayed.
        - alpha (optional): Sets the alpha value of the image to fade into while displaying
        """
        self.img.set_alpha(self.init_alpha)
        if self.init_alpha > alpha+10:
            self.init_alpha-=10
        elif alpha == 255:
            self.reset_alpha()

        if self.anim_scale:
            self.img = pygame.transform.smoothscale(self.source, (self.w, self.h))
        if self.anim_rot:
            self.img = pygame.transform.rotozoom(self.source, self.rotation, 0.75)
            self.rotated_image_rect = self.img.get_rect(center = self.surface_center)
            self.surface.blit(self.img, self.rotated_image_rect)
            return
            
        self.surface.blit(self.img, (self.x, self.y))
        
    def get_rect(self):
        return self.img.get_rect(topleft=(self.x, self.y))