import pygame
from .new_btn import NButton
from .rect_window import RectWindow

class ModeWindow:

    def __init__(self, surface: pygame.Surface, pos: tuple, 
                    width: float, height: float, color, *, 
                    border_radius: int, border_thickness: int,
                    border_color, button_text: str, button_pos: tuple, 
                    button_width: float, button_height: float, 
                    button_shadow_offset: int):

                self.surface = surface
                self.x, self.y = self.pos = pos
                self.w, self.h = self.width, self.height = width, height
                self.color = color
                self.border_radius = border_radius
                self.border_thickness = border_thickness
                self.border_color = border_color

                self.button_text = button_text
                self.button_pos = button_pos
                self.button_width = button_width
                self.button_height = button_height
                self.button_shadow_offset = button_shadow_offset

                self.rect_window = RectWindow(self.surface, self.pos,
                                    self.w, self.h, self.color, self.border_radius,
                                    self.border_thickness, self.border_color, False)

                self.expand_btn = NButton(self.surface, self.button_pos,
                                    self.button_width, self.button_height,
                                    text=self.button_text, shadow_offset=self.button_shadow_offset)

    def draw(self):

        self.rect_window.draw()
        self.expand_btn.draw((self.rect_window.x+
                        self.rect_window.w*0.5-
                        self.expand_btn.get_rect().w*0.5, 
                        self.rect_window.y+
                        self.rect_window.h-
                        self.expand_btn.get_rect().h*0.5))                


    