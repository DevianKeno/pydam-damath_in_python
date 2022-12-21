import pygame, time
import pytweening
from ui_class import tween as tween
from ui_class.ease_funcs import *
from display_constants import SIDE_MENU_COLOR, BG_COLOR, SCREEN_WIDTH
from damath.constants import WHITE

class SideMenuAnim:

    def __init__(self, surface, initial_rect, updated_rect):
        self.surface = surface
        self.initial_rect = initial_rect
        self.updated_rect = updated_rect

        #self.diff = self.updated_rect.width - self.initial_rect.width
        self.init_width = self.initial_rect.width
        self.max_width = self.init_width

        self.next_anim = 0
        self.anim_idx = 0
        self.reversed_anim_idx = 0
        self.is_finished = False
        self.reversed_is_finished = False
        self.added_width = 0
        self.subtracted_width = 0
        self.ease = []

        self.play_has_easing_list = False
        self.reverse_has_easing_list= False

    def easing(self, diff):
        for i in range (0, int(diff), 25):
            self.ease.append(pytweening.easeInOutSine(i/diff)*(diff))

    def play(self):
        
        if not self.play_has_easing_list:
            self.ease.clear()
            self.easing(self.updated_rect.width - (self.init_width + self.added_width))
            self.play_has_easing_list = True
        
        self.reverse_has_easing_list = False
        time_now = pygame.time.get_ticks()
        self.reversed_anim_idx = 0
        self.reversed_is_finished = False
        #self.subtracted_width = 0

        if not self.is_finished:
            if time_now > self.next_anim:
                if len(self.ease) > 0:
                    if self.added_width < (self.updated_rect.width - (self.init_width)):
                        self.next_anim = time_now + 1
                        self.added_width = self.ease[self.anim_idx]
                        self.max_width = self.init_width + self.added_width

                if self.anim_idx <= len(self.ease) - 2:
                    self.anim_idx += 1
                else:
                    self.is_finished = True
                    self.anim_idx = 0

        self.initial_rect.update(self.initial_rect.x, self.initial_rect.y, self.max_width, self.initial_rect.height)
        pygame.draw.rect(self.surface, SIDE_MENU_COLOR, self.initial_rect)

    def reverse_play(self):

        if not self.reverse_has_easing_list:
            self.ease.clear()
            self.easing(self.added_width)
            self.reverse_has_easing_list = True

        self.play_has_easing_list = False
        self.is_finished = False
        self.anim_idx = 0
        #self.added_width = 0
        time_now = pygame.time.get_ticks()

        if not self.reversed_is_finished:
            if time_now > self.next_anim:
                if len(self.ease) > 0:
                    if self.subtracted_width < self.added_width:
                        self.next_anim = time_now + 1
                        self.subtracted_width = self.ease[self.reversed_anim_idx]
                        self.max_width = (self.init_width + self.added_width) - self.subtracted_width            
            if self.reversed_anim_idx <= len(self.ease) - 2:
                self.reversed_anim_idx += 1
            else:
                self.reversed_is_finished = True
                self.added_width = 0
                self.reversed_anim_idx = 0

        self.initial_rect.update(self.initial_rect.x, self.initial_rect.y, self.max_width, self.initial_rect.height)
        pygame.draw.rect(self.surface, SIDE_MENU_COLOR, self.initial_rect)

    def display(self):    
        pygame.draw.rect(self.surface, SIDE_MENU_COLOR, self.initial_rect)

    def reset(self):
        self.initial_rect.update(self.initial_rect.x, self.initial_rect.y, self.init_width, self.initial_rect.height)
        self.added_width = 0
        self.next_anim = 0
        self.anim_idx = 0
        self.is_finished = False
        pygame.draw.rect(self.surface, SIDE_MENU_COLOR, self.initial_rect)

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
                self.frame.blit(hover_font.render(str(hovertext), True, WHITE), (0, (self.fontsize+(self.fontsize*0.14))+(int(0.42*self.fontsize)*idx)))

    def hover_update(self, target=None):

        # self.hover_anim = tween.Move(self, (self.x, self.y+40), 0.1, ease_type=easeInSine)
        # self.hover_anim.play()
        # self.hover_anim.update()
        self.text_surface = self.font.render(self.text, True, WHITE)
        self.frame.blit(self.text_surface, (0, 0))
        
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

