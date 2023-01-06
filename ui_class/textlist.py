import pygame
from ui_class.colors import *

FONT_SIZE = 20
font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(FONT_SIZE))

class TextList:
    """
    Display a vertical lists of text for dropdowns or menus.
    """
    
    def __init__(self, font, font_color=BLACK, list=[], icons=[], rect=None, padding=0, icon_padding=0):
        self.font = font_cookie_run_reg
        self.font_color = font_color
        self.text_list = list
        self.icon_list = icons
        self.rect = rect
        self.padding = padding
        self.icon_padding = icon_padding
        self.HasIcons = False
        if icons:
            self.HasIcons = True
            self.icons_count = len(self.icon_list)

    def draw_vertical(self, surface, pos):
        """
        Draw a vertical text list.
        """
        if self.HasIcons:
            x = pos[0] + self.icon_list[0].w + self.icon_padding
        else:
            x = pos[0]
        y = pos[1]

        items_count = len(self.text_list)

        for i in range(items_count):
            textlist_item_surface = self.font.render(self.text_list[i], True, self.font_color)
            textlist_item_rect = textlist_item_surface.get_rect(topleft=(x, y))
            surface.blit(textlist_item_surface, textlist_item_rect)
            y += textlist_item_rect.h + self.padding
            
            if not self.HasIcons:
                continue

            icon = self.icon_list[i]
            icon.x = pos[0] 
            icon.y = textlist_item_rect.centery - icon.h//2
            icon.display()
            

    def draw_horizontal(self, surface, pos):
        """
        Draw a horizontal text list.
        """
        if self.HasIcons:
            x = pos[0] + self.icon_list[0].w
        else:
            x = pos[0]
        y = pos[1]

        items_count = len(self.text_list)

        for i in range(items_count):
            textlist_item_surface = self.font.render(self.text_list[i], True, self.font_color)
            textlist_item_rect = textlist_item_surface.get_rect(topleft=(x, y))
            surface.blit(textlist_item_surface, textlist_item_rect)
            x += textlist_item_rect.w + self.padding
            
            if not self.HasIcons:
                continue

            icon = self.icon_list[i]
            x += icon.w
            icon.x = textlist_item_rect.left - icon.h
            icon.y = textlist_item_rect.centery - icon.h//2
            icon.display()


