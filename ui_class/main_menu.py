import pygame, time
import pytweening
from ui_class import tween as tween
from ui_class.ease_funcs import *
from display_constants import SIDE_MENU_COLOR, BG_COLOR, SCREEN_WIDTH

class SideMenu:
    
    def __init__(self):
        pass


class MainMenu:
    
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

        self.hover_anim = None
        self.next_anim = 0
        self.anim_idx = 0
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
            hover_font = pygame.font.Font('font\CookieRun_Regular.ttf', int(0.42*self.fontsize))
            for idx, hovertext in enumerate(self.hover_text):
                self.frame.blit(hover_font.render(str(hovertext), True, self.color), (0, (self.fontsize+(self.fontsize*0.14))+(int(0.42*self.fontsize)*idx)))

    def hover_update(self, target=None):

        # self.hover_anim = tween.Move(self, (self.x, self.y+40), 0.1, ease_type=easeInSine)
        # self.hover_anim.play()
        # self.hover_anim.update()

        self.is_hovered = True
        self.hover_height = self.height + int(self.height/2)
        time_now = pygame.time.get_ticks()

        ease = []
        for i in range(6):
            ease.append(pytweening.easeInOutSine(i/5)*20)

        if (time_now > self.next_anim):
            if self.hover_y <= int(self.hover_height/2):
                self.next_anim = time_now + 10
                self.rect.update(self.x, self.y-ease[self.anim_idx], self.width, self.hover_height)
            self.hover_y += ease[self.anim_idx]
            
            if self.anim_idx <= len(ease)-2:
                self.anim_idx += 1
            else:
                self.next_anim = 0

        if target is not None:
            if pygame.mouse.get_pressed()[0]:
                target()

    def reset(self):
        self.anim_idx = 0
        self.is_hovered = False
        self.hover_y = 1
        self.next_anim = 0
        self.rect.update(self.x, self.y, self.width, self.height)

