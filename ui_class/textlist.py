import pygame
from ui_class.colors import *

FONT_SIZE = 20
font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(FONT_SIZE))

class TextList:
    """
    List of text object for dropdowns or menus.
    """
    
    def __init__(self, font, font_color=BLACK, list=[], icons=[], spacing=0, icon_spacing=0, padding=[0, 0, 0, 0], vertical=True):
        self.font = font
        self.font_color = font_color
        self.item_list = list
        self.items_count = len(self.item_list)
        self.icon_list = icons
        self.icons_count = 0
        self.HasIcons = False
        self.spacing = spacing
        self.icon_spacing = icon_spacing
        self.padding = padding
        self.IsVertical = vertical
        self.text_rects = []
        self.IsActive = True

        if icons:
            self.HasIcons = True
            self.icons_count = len(self.icon_list)
            
        self.pos = (0, 0)
        self.x = self.pos[0]
        self.y = self.pos[1]

        """
        Gets the longest string which the window's width will be based on.
        """
        self.longest_item = max(list, key=len)
        self.longest_item_index = list.index(self.longest_item)
        self.longest_item_surface = self.font.render(self.item_list[self.longest_item_index], True, self.font_color)
        self.longest_item_rect = self.longest_item_surface.get_rect(topleft=(0, 0))
        self.longest_item_rect = self.longest_item_surface.get_rect(topleft=(0, 0), width=self.longest_item_rect.w + (self.padding[1]+self.padding[2]))

        if self.HasIcons:
            self.longest_item_rect = self.longest_item_surface.get_rect(topleft=(0, 0), width=self.longest_item_rect.w +(self.padding[1]+self.padding[2])+self.icon_list[0].w)

    def generate_rects(self, pos):
        """
        Called when the list is first shown.
        """
        
        x = pos[0] + self.padding[1]
        y = pos[1] + self.padding[0]

        for i in range(self.items_count):
            textlist_item_surface = self.font.render(self.item_list[i], True, self.font_color)
            textlist_item_rect = textlist_item_surface.get_rect(topleft=(x, y), width=self.longest_item_rect.w)
            self.text_rects.append(textlist_item_rect)

            if self.IsVertical:
                y += textlist_item_rect.h + self.spacing
            else:
                x += textlist_item_rect.w + self.spacing
        

    def draw(self, surface, pos):
        if not self.IsActive:
            return

        if self.IsVertical:
            self._draw_vertical(surface, pos)
        # else:
        #     self._draw_horizontal(surface, pos)


    def _draw_vertical(self, surface, pos):
        """
        Draw a vertical text list.
        """
        
        self.text_x = pos[0] + self.padding[1]
        self.text_y = pos[1] + self.padding[0]

        if self.HasIcons:
            self.text_x = pos[0] + self.padding[1] + self.icon_list[0].w + self.icon_spacing
            self.icon_x = pos[0] + self.padding[1]

        for i in range(self.items_count):
            textlist_item_surface = self.font.render(self.item_list[i], True, self.font_color)
            textlist_item_rect = textlist_item_surface.get_rect(topleft=(self.text_x, self.text_y))
            surface.blit(textlist_item_surface, textlist_item_rect)
            self.text_y += textlist_item_rect.h + self.spacing
            
            if not self.HasIcons:
                continue

            icon = self.icon_list[i]
            icon.x = self.icon_x
            icon.y = textlist_item_rect.centery - icon.h//2
            icon.display()

    """
    Needs fixing but probably won't use
    """
    # def _draw_horizontal(self, surface, pos):
    #     """
    #     Draw a horizontal text list.
    #     """
    #     self.x = pos[0] + self.icon_list[0].w + self.icon_spacing
    #     self.y = pos[1]

    #     for i in range(self.items_count):
    #         textlist_item_surface = self.font.render(self.item_list[i], True, self.font_color)
    #         textlist_item_rect = textlist_item_surface.get_rect(topleft=(self.x, self.y))
    #         surface.blit(textlist_item_surface, textlist_item_rect)
    #         self.x += textlist_item_rect.w + self.spacing
            
    #         if not self.HasIcons:
    #             continue

    #         icon = self.icon_list[i]
    #         self.x += icon.w + self.icon_spacing
    #         icon.x = textlist_item_rect.left - icon.h
    #         icon.y = textlist_item_rect.centery - icon.h//2
    #         icon.display()

    def get_rect(self, index):
        return self.text_rects[index]

    def _draw_hover(self, index):
        pass