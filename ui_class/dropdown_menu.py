



import pygame
from ui_class.colors import *
from ui_class.rect_window import RectWindow

window_min_width = 200
window_min_height = 100
window_color = DARK_CERULEAN

class Dropdown:

    def __init__(self, surface, text_list, IsSelectable=True, targets=[]) -> None:
        self.surface = surface
        self.text_list = text_list
        self.IsSelectable = IsSelectable
        self.targets = targets
        self.IsActive = True

        self.selected = None

        self.window = RectWindow(surface, (0, 0), window_min_width, window_min_width, window_color, 9, 4, WHITE)

        """
        Create the rounded rect displayed when hovering.
        """

    def create(self, pos, color=None):
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
    
        if color == None:
            window_color = DARK_CERULEAN
        else:
            window_color = color

        self.text_list.generate_rects(pos)

        self.text_rect = self.text_list.longest_item_rect
        window_new_width = (self.text_rect.w + 
                            (self.text_list.padding[1] + self.text_list.padding[2]))

        # if self.text_list.HasIcons:
        #     window_new_width += (self.text_list.icon_spacing + self.text_list.icon_list[0].w)

        window_new_height = ((self.text_list.items_count * self.text_rect.h) +
                            (self.text_list.items_count * self.text_list.spacing) +
                            (self.text_list.padding[0] + self.text_list.padding[1]))

        self.window = RectWindow(self.surface, self.pos, window_new_width, window_new_height, window_color, 9, 4, WHITE)

    def draw(self):
        if not self.IsActive:
            return

        self.window.draw()
        self.text_list.draw(self.surface, self.pos)

        if self.IsSelectable:
            m_pos = pygame.mouse.get_pos()
            self._check_for_hover(m_pos)

    def _check_for_hover(self, m_pos):
        for i in range(self.text_list.items_count):
            item_rect = self.text_list.get_rect(i)
            if item_rect.collidepoint(m_pos):
                self.selected = i
                hover_area = pygame.Surface((item_rect.w, item_rect.h))
                hover_area.set_alpha(64)
                hover_area.fill((255, 255, 255))
                self.surface.blit(hover_area, item_rect)

    def get_selected(self):
        return self.selected