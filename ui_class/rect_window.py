from __future__ import annotations
import pygame
from .colors import *

class RectWindow(pygame.Rect):
    def __init__(self, surface: pygame.Surface,
                    pos: tuple, width: float, height: float, 
                    color, border_radius: int,
                    border_thickness: int,
                    border_color, cast_shadow: bool=True):
        """
        Creates a Window using pygame's built-in Rect
        
        This class will inherit the pygame.Rect class
        which will serve as the outer rect for the window.

        The inner rect will be created inside this class 
        and all attributes relating only to the inner rect 
        will be indicated by the prefix 'inner'.

        All methods of the Window class similar to the 
        parent class will also be indicated by
        the prefix 'w'. New class methods however will not 
        have a prefix on it.

        Any other remaining methods is part of the parent 
        class and is therefore only limited to the outer rect 
        of the Window.

        Window methods:
            - wmove (move window in place)
            - winflate (inflates the window in place)
            - wupdate (updates the window's position and size)
            - change_color (changes the color of the window / border)
            - change_thickness (changes the thickness of the window's border)
            - change_radius (changes the border radius of the window)

        Inner rect-only methods:
            - self.inner_rect.[pygame.Rect methods]            

        Outer rect-only methods:
           - self.[pygame.Rect methods] or self.rect.[pygame.Rect methods]

        """
        super().__init__(pos[0], pos[1], width, height)
        self.surface = surface
        self.color = color
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.cast_shadow = cast_shadow
        self._rect()

    def _rect(self):
        self.rect = self
        if self.cast_shadow:
            self.shadow_surf_rect = pygame.Rect(self.x+8, self.y+8, self.w, self.h)
            self.shadow_surf = pygame.Surface((self.shadow_surf_rect.w, self.shadow_surf_rect.h))
            self.shadow_surf.set_colorkey((0, 0, 0))
            self.shadow_surf.set_alpha(100)
            self.shadow_rect = pygame.Rect(0, 0, self.w, self.h)
        self.inner_rect = pygame.Rect(self.x, self.y, 
                            self.w-self.border_thickness, self.h-self.border_thickness)
        self.inner_rect.center = self.center

    def draw(self):

        if self.cast_shadow:
            # shadow
            self.surface.blit(self.shadow_surf, (self.shadow_surf_rect.x, self.shadow_surf_rect.y))
            pygame.draw.rect(self.shadow_surf, DARK_GRAY_BLUE, 
                            self.shadow_rect, border_radius=self.border_radius)

        # outer rect (border)
        pygame.draw.rect(self.surface, self.border_color, 
                        self.rect, border_radius=self.border_radius)
        # inner rect
        pygame.draw.rect(self.surface, self.color,
                        self.inner_rect, border_radius=self.border_radius)

    def wmove(self, x, y):
        """
        Moves the window to the specified position (in place)
        """
        super().move_ip(x, y)
        self.inner_rect.center = self.center

    def winflate(self, x, y):
        """
        Grows or shrinks the window depending on
        the given offset
        """
        self.inflate_ip(x, y)
        self.inner_rect.inflate_ip(x, y)

    def wupdate(self, x=-1, y=-1, width=-1, height=-1):
        if x == -1:
            _new_x = self.x
        else:
            _new_x = x
            
        if y == -1:
            _new_y = self.y
        else:
            _new_y = y

        if width == -1:
            _new_width = self.width
        else:
            _new_width = width

        if height == -1:
            _new_height = self.height
        else:
            _new_height = height

        self.update(_new_x, _new_y, _new_width, _new_height)
        self.inner_rect.update(_new_x, _new_y,  
                    _new_width-self.border_thickness, 
                    _new_height-self.border_thickness)
        self.inner_rect.center = self.center
        
        if self.cast_shadow:
            self.shadow_surf_rect.update(_new_x+8, _new_y+8, _new_width, _new_height)

    def change_color(self, *, window_color=None, border_color=None):
        if window_color is None:
            window_color = self.color
        if border_color is None:
            border_color = self.border_color

        if window_color is None and border_color is None:
            return

        self.color = window_color
        self.border_color = border_color

    def change_thickness(self, border_thickness: int):
        if border_thickness < 0:
            raise ValueError("border_thickness must be less than zero")

        self.border_thickness = border_thickness
        self._rect()

    def change_radius(self, border_radius: int):
        self.border_radius = border_radius
        self._rect()

def create_window(surface, pos: tuple,
                    width, height, color, *,
                    border_radius: int = 20,
                    border_thickness: int = 4,
                    border_color = WHITE, 
                    cast_shadow = True):
    """
    Optional Keyword-Only Arguments:
        - border_radius (Default: 20)
        - border_thickness (Default: 4)
        - border_color (Default: WHITE)

    Returns a RectWindow object
    """

    return RectWindow(surface, pos, width, 
            height, color, border_radius,
            border_thickness, border_color,
            cast_shadow)
