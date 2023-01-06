import pygame
from damath.constants import PLAYER_ONE, PLAYER_TWO
from damath.piece import Piece
from objects import font_cookie_run_reg, cheats_window_blue, cheats_window_orange, cheats_window_blue_long, cheats_window_orange_long, icon_add, icon_remove, icon_promote, icon_demote
from ui_class.colors import *

FONT_SIZE = cheats_window_blue.h * 0.25
font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(FONT_SIZE))

class TextList:
    """
    Display a vertical lists of text for dropdowns or menus.
    """
    
    def __init__(self, font, font_size, list=[], rect=None, padding=0):
        self.font = font
        self.font_size = font_size
        self.text_list = list
        self.rect = rect
        self.padding = padding

    def draw(self, surface, pos):
        x = pos[0]
        y = pos[1]
        items_count = len(self.text_list)
        item_height = self.rect.h//(items_count+1)

        for i in range(items_count):
            textlist_item_surface = self.font.render(self.text_list[i], True, WHITE)
            textlist_item_rect = textlist_item_surface.get_rect(left=(x+self.rect.w*0.3), centery=(y+(i+1)*item_height))
            surface.blit(textlist_item_surface, textlist_item_rect)

class Cheats:
    """
    Cheats.
    """
    
    def __init__(self, surface):
        self.surface = surface
        self.ShowWindow = False
        self.piece = Piece(surface, 0, 0, 0, 0)
        self.pos = ()
        self.textlist_options = []
        self.icons = []
        self.window_rect = pygame.Rect(0, 0, cheats_window_blue.w, cheats_window_blue.h)

        self.font = pygame.font.Font('font\CookieRun_Regular.ttf', int(FONT_SIZE))

    def show_window(self, pos, row, col, board):
        self.ShowWindow = True
        self.pos = pos
        self.piece = board[row][col]
            
        if self.piece.color == 0:
            self.window = cheats_window_blue_long
            self.textlist_options = ["Add Blue", "Add Orange"]
            self.icons = [icon_add, icon_add]
        else:
            self.var = cheats_window_blue
            if not self.piece.IsKing:
                self.textlist_options = ["Remove", "Promote"]
                self.icons = [icon_remove, icon_promote]
                pass
            else:
                self.textlist_options = ["Remove", "Demote"]
                self.icons = [icon_remove, icon_demote]
                pass
        
        self.textlist = TextList(self.font, FONT_SIZE, self.textlist_options, self.window_rect)

    def draw(self):
        if not self.ShowWindow:
            return
            
        self.icons_count = len(self.icons)
        self.icon_div_height = self.window_rect.h//(self.icons_count+1)

        if self.piece.color == 0:
            self.window.display(self.pos)
            self.textlist.draw(self.surface, self.pos)
            for i, icon in enumerate(self.icons):
                icon.x = self.pos[0] + self.window_rect.w*0.08 
                icon.y = self.pos[1] + (i+1) * self.icon_div_height - icon.h//2
                icon.display()
        else:
            if self.piece.color == PLAYER_ONE:
                cheats_window_blue.display(self.pos)
                self.textlist.draw(self.surface, self.pos)

                for i, icon in enumerate(self.icons):
                    icon.x = self.pos[0] + self.window_rect.w*0.08 
                    icon.y = self.pos[1] + (i+1) * self.icon_div_height - icon.h//2
                    icon.display()
            else:
                cheats_window_orange.display(self.pos)
                self.textlist.draw(self.surface, self.pos)
                
                for i, icon in enumerate(self.icons):
                    icon.x = self.pos[0] + self.window_rect.w*0.08 
                    icon.y = self.pos[1] + (i+1) * self.icon_div_height - icon.h//2
                    icon.display()

    def draw_hover(self):
        pass

    def remove(self, piece):
        pass

    def add_piece(self, piece):
        pass

    def promote(self, piece):
        pass

    def demote(self, piece):
        pass

    pass