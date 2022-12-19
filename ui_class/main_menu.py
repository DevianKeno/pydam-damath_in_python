import pygame, time
from display_constants import SIDE_MENU_COLOR, BG_COLOR
class MainMenuOptions:
    
    def __init__ (self, surface, pos, width, height, text, color, fontsize, target, args=[], hover_text=[]):
        self.x, self.y = pos
        self.surface = surface
        self.width = width
        self.height = height
        self.text = text
        self.hover_text = hover_text
        self.color = color
        self.fontsize = fontsize
        self.target = target
        self.args = args
        self.next_anim = 0
        self.hover_y = 1
        self.text_surface = None
        self.is_hovered = False
        self._init()

    def _init(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.frame = pygame.Surface((self.rect.w, self.rect.h))
        self.font = pygame.font.Font('font/CookieRun_Regular.ttf', self.fontsize)

    def display(self):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.surface.blit(self.frame, (self.rect.x, self.rect.y))
        self.frame.fill(SIDE_MENU_COLOR)
        self.frame.blit(self.text_surface, (0, 0))

        if self.is_hovered:
            hover_font = pygame.font.Font('font\CookieRun_Regular.ttf', 14)
            for idx, hovertext in enumerate(self.hover_text):
                self.frame.blit(hover_font.render(str(hovertext), True, BG_COLOR), (0, 50+(14 *idx)))

    def hover_update(self):
        self.hover_height = self.height + 40
        time_now = pygame.time.get_ticks()

        if (time_now > self.next_anim):
            if self.hover_y <= 20:
                self.next_anim = time_now + 10
                self.rect.update(self.x, self.y-self.hover_y, self.width, self.hover_height)
                self.hover_y += 2
            self.is_hovered = True

    def reset(self):
        self.is_hovered = False
        self.hover_y = 1
        self.next_anim = 0
        self.rect.update(self.x, self.y, self.width, self.height)

