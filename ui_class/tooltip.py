from typing import List
import time
import pygame
from pygame import gfxdraw
from assets import CURSOR
from .colors import *
from .font import *

class Tooltip:
    
    def __init__(self, surface, x, y, width, height, rect_color, text_color, text,
                    cast_shadow=True, shadow_offset=10):
        
        #TODO: Allow for multi-line texts in tooltip
        self.surface = surface
        self.tltp_x = x
        self.tltp_y = y
        self.tltp_w = self.tltp_width = width
        self.tltp_h = self.tltp_height = height
        self.rect_color = rect_color
        self.text_color = text_color
        self.tltp_text = text

        self.cast_shadow = cast_shadow
        self.tltp_shadow_offset = shadow_offset

        self.tltp_rect_shadow = pygame.Rect(self.tltp_x+self.tltp_shadow_offset, self.tltp_y+self.tltp_shadow_offset, self.tltp_w, self.tltp_h)
        self.tltp_rect = pygame.Rect(self.tltp_x, self.tltp_y, self.tltp_w, self.tltp_h)

        self.tltp_font = pygame.font.Font(CookieRun_Regular, int(self.tltp_h*0.3))
        self._init()

    def _init(self):

        self.start_sec = False
        self.sec_idx = 0

        self.mouse_init_pos = None
        self.starttime_checked = 0
        self.currenttime_checked = 0

    def _show(self, alpha: int=255):

        gfxdraw.box(self.surface, self.tltp_rect_shadow, (180, 180, 180, 150))
        gfxdraw.box(self.surface, self.tltp_rect, pygame.Color(self.rect_color))
        gfxdraw.rectangle(self.surface, self.tltp_rect, pygame.Color(WHITE))

        text = self.tltp_font.render(self.tltp_text, True, self.text_color)

        self.surface.blit(text, (self.tltp_rect.x+
                self.tltp_rect.w*0.5-(text.get_width()*0.5), 
                self.tltp_rect.y+self.tltp_h*0.5-(text.get_height()*0.5)))

        #TODO: Add fade effect
        #TODO: Must be aware if the rect will exceed SCREEN_WIDTH to show the rect on the left side of the cursor instead

    def show_tooltip(self, after_sec: int):

        if not self.start_sec:
            self.mouse_init_pos = pygame.mouse.get_pos()
            self.starttime_checked = time.time()
            self.start_sec = True
            self.tltp_rect_shadow.update(self.mouse_init_pos[0]+CURSOR.get_width()+self.tltp_shadow_offset, self.mouse_init_pos[1]+CURSOR.get_height()+self.tltp_shadow_offset, self.tltp_w, self.tltp_h)
            self.tltp_rect.update(self.mouse_init_pos[0]+CURSOR.get_width(), self.mouse_init_pos[1]+CURSOR.get_height(), self.tltp_w, self.tltp_h)
            
        else:
            self.currenttime_checked = (time.time() - self.starttime_checked)

            if self.currenttime_checked >= after_sec:

                if pygame.mouse.get_pos() == self.mouse_init_pos:
                    self._show()

                else:
                    self.reset()
    
    def reset(self):
        self._init()

        


        


    



        