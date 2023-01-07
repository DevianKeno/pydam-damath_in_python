import pygame, time
import pytweening
from .constants import BTN_PRESSED_COLOR
from ui_class import tween as tween
from ui_class.ease_funcs import *
from display_constants import SIDE_MENU_COLOR, SIDE_MENU_RECT_ACTIVE, SIDE_MENU_RECT_DEFAULT, FPS
from damath.constants import WHITE, DARK_GRAY_BLUE

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
        self.reversed_is_playing = False
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
        self.reversed_is_playing = False
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
            self.reversed_is_playing = True
            if time_now > self.next_anim:
                if len(self.ease) > 0:
                    if self.subtracted_width < self.added_width:
                        self.next_anim = time_now + 1
                        self.subtracted_width = self.ease[self.reversed_anim_idx]
                        self.max_width = (self.init_width + self.added_width) - self.subtracted_width            
            if self.reversed_anim_idx <= len(self.ease) - 2:
                self.reversed_anim_idx += 1
            else:
                self.reversed_is_playing = False
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
        self.selected = False 
        self._init()

    def _init(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.frame = pygame.Surface((self.rect.w, self.rect.h))
        self.font = pygame.font.Font('font/CookieRun_Regular.ttf', self.fontsize)

    def display(self):
        if not self.selected:
            self.text_surface = self.font.render(self.text, True, self.color)
        else:
            self.text_surface = self.font.render(self.text, True, BTN_PRESSED_COLOR)

        self.surface.blit(self.frame, (self.rect.x, self.rect.y))
        self.frame.fill(SIDE_MENU_COLOR)
        self.frame.blit(self.text_surface, (0, 0))

        if self.is_hovered:
            hover_font = pygame.font.Font('font\CookieRun_Regular.ttf', int(0.42*self.fontsize))

            for idx, hovertext in enumerate(self.hover_text):
                if self.selected:
                    self.frame.blit(hover_font.render(str(hovertext), True, BTN_PRESSED_COLOR), (0, (self.fontsize+(self.fontsize*0.14))+(int(0.42*self.fontsize)*idx)))
                else:
                    self.frame.blit(hover_font.render(str(hovertext), True, WHITE), (0, (self.fontsize+(self.fontsize*0.14))+(int(0.42*self.fontsize)*idx)))

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def hover_update(self, target=None):

        # self.hover_anim = tween.Move(self, (self.x, self.y+40), 0.1, ease_type=easeInSine)
        # self.hover_anim.play()
        # self.hover_anim.update()
        if self.selected:
            self.text_surface = self.font.render(self.text, True, BTN_PRESSED_COLOR)
        else:
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
                self.select()
                target()
            else:
                self.unselect()

    def get_text_rect(self):
        return self.text_surface.get_rect(left=self.rect.x, top=self.rect.y, height=self.rect.h/1.65)

    def reset(self):
        self.anim_idx = 0
        self.is_hovered = False
        self.hover_y = 1
        self.next_anim = 0
        self.rect.update(self.x, self.y, self.width, self.height)

state, status = str, str
class Sidebar: 

    dt = pygame.time.Clock().tick(FPS)/1000
    diff = SIDE_MENU_RECT_ACTIVE.width - SIDE_MENU_RECT_DEFAULT.width
    
    Hovered = 'Hovered'
    Normal = 'Normal'

    Default = 'Default'
    Animating = 'Animating'
    Active = 'Active'

    def __init__(self, surface: pygame.Surface, 
                pos: tuple, width: float, height: float,
                color=DARK_GRAY_BLUE, fontstyle='font\CookieRun_Regular.ttf', 
                fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.045),
                anim_duration: int=8):

                self.surface = surface
                self.x, self.y = pos
                self.w, self.h = self.width, self.height = width, height
                self.color = color
                self.fontstyle = fontstyle
                self.fontsize = fontsize

                self.anim_duration = anim_duration
                self.anim_idx = 0

                self.current_w = width
                self.init_w = width
                self.options_counter = 0

                self.font = pygame.font.Font(fontstyle, fontsize)
                self._init()

    def _init(self):

        self._STATUS = {self.Default: True,
            self.Animating: False,
            self.Active: False}

        self._STATES = {self.Hovered: False,
            self.Normal: True}

        self.state = self.Normal
        self.status = self.Default
        self.sidebar_rect = pygame.Rect(self.x, self.y, 
                                self.w, self.h)
        
        self.anim_move = (self.diff/self.anim_duration)

    def _draw(self, nwidth=None, nheight=None):
        
        if nwidth is None:
            nwidth = self.w
        if nheight is None:
            nheight = self.h
        
        self.sidebar_rect.update(self.x, self.y, nwidth, nheight)
        pygame.draw.rect(self.surface, self.color, self.sidebar_rect)

        if self.get_status() == self.Active:
            text = self.font.render('Play', True, WHITE)
            self.surface.blit(text, (50, 50))

    def _animate(self):
        
        if self.state == self.Normal:
            if self.current_w > self.init_w:
                self.current_w-=self.anim_move
            if self.anim_idx > 0:
                self.anim_idx-=1
                self.set(status=self.Animating)
            else:
                self.set(status=self.Default)

        else:
            if self.current_w < (self.init_w + self.diff):
                self.current_w+=self.anim_move
            if self.anim_idx < self.anim_duration:
                self.anim_idx+=1
                self.set(status=self.Animating)
            else:
                self.set(status=self.Active)

        self._draw(self.current_w)

    def set(self, *, state=None, status=None):
        """
        Sets a state or a status for the sidebar
        """
        pass

        if state is not None:
            if state not in self._STATES.keys():
                raise ValueError(f'Invalid State.' \
                                f'Expected one of the following: {self._STATES}')

            for key_state in self._STATES.keys():
                if key_state != state:
                    self._STATES[key_state] = False
                else:
                    self._STATES[key_state] = True
            
            self.state = state
            self._animate()

        if status is not None:
            if status not in self._STATUS.keys():
                raise ValueError(f'Invalid Status.' \
                                    f'Expected one of the following: {self._STATUS}')
                
            for key_status in self._STATUS.keys():
                if key_status != status:
                    self._STATUS[key_status] = False
                else:
                    self._STATUS[key_status] = True       

            self.status = status

    def get_state(self) -> state:
        """
        Returns the current state of the sidebar
        """
        for key_state in self._STATES.keys():
            if self._STATES[key_state]:
                return key_state

    def get_status(self) -> status:
        """
        Returns the current status of the sidebar
        """
        for key_status in self._STATUS.keys():
            if self._STATUS[key_status]:
                return key_status

    def get_rect(self) -> pygame.Rect:
        """
        Returns the rect of the sidebar
        """
        return self.sidebar_rect