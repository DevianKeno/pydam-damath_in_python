import pygame
from damath.constants import PLAYER_ONE, PLAYER_TWO
from damath.piece import Piece
from objects import font_cookie_run_reg, cheats_window_blue, cheats_window_orange, cheats_window_blue_long, cheats_window_orange_long, icon_add, icon_remove, icon_promote, icon_demote
from ui_class.colors import *
from ui_class.textlist import TextList

FONT_SIZE = cheats_window_blue.h * 0.25
font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(FONT_SIZE))

class Cheats:
    """
    Cheats.
    """
    
    def __init__(self, surface):
        self.surface = surface
        self.ShowWindow = False
        self.piece = Piece(surface, 0, 0, 0, 0)
        self.pos = ()
        self.items = []
        self.icons = []
        self.window_rect = pygame.Rect(0, 0, cheats_window_blue.w, cheats_window_blue.h)

        self.font = pygame.font.Font('font\CookieRun_Regular.ttf', int(FONT_SIZE))
        self.text_list = None
        self.selected = 0

    def show_window(self, pos, row, col, board):
        self.ShowWindow = True
        self.pos = pos
        self.piece = board[row][col]
            
        if self.piece.color == 0:
            self.window = cheats_window_blue_long
            self.items = ["Add Blue", "Add Orange"]
            self.icons = [icon_add, icon_add]
        else:
            if not self.piece.IsKing:
                self.items = ["Remove", "Promote"]
                self.icons = [icon_remove, icon_promote]
            else:
                self.items = ["Remove", "Demote"]
                self.icons = [icon_remove, icon_demote]
        
            if self.piece.color == PLAYER_ONE:
                self.window = cheats_window_blue
            else:
                self.window = cheats_window_orange
        
        self.text_list = TextList(font_cookie_run_reg, WHITE, self.items, self.icons, spacing=5, icon_spacing=10, padding=10)
        self.text_list.generate_rects(pos, self.window)

    def draw(self):
        if not self.ShowWindow:
            return

        if self.piece.color == 0:
            self.window.display(self.pos)
            self.text_list.draw(self.surface, self.pos)
        else:
            if self.piece.color == PLAYER_ONE:
                self.window.display(self.pos)
                self.text_list.draw(self.surface, self.pos)
            else:
                self.window.display(self.pos)
                self.text_list.draw(self.surface, self.pos)
    
    def check_for_hover(self, m_pos):
        for i in range(self.text_list.items_count):
            item_rect = self.text_list.get_rect(i)
            if item_rect.collidepoint(m_pos):
                self.selected = i + 1
                pygame.draw.rect(self.surface, BLACK, item_rect)

    def invoke(self):
        match self.selected:
            case 0:
                pass
            case 1:
                print("1")
                self.add_piece()
                pass
            case 2:
                print("2")
                self.remove()
                pass
            case 3:
                print("3")
                self.promote()
                pass
            case 4:
                print("4")
                self.demote()  
                pass

    def add_piece(self, piece):
        pass

    def remove(self, piece):
        pass

    def promote(self, piece):
        pass

    def demote(self, piece):
        pass

    pass