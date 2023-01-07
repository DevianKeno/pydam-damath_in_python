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
    
    def __init__(self, surface, game):
        self.surface = surface
        self.game = game
        self.ShowWindow = False
        self.piece = Piece(surface, 0, 0, 0, 0)
        self.pos = ()
        self.items = []
        self.icons = []
        self.window_rect = pygame.Rect(0, 0, cheats_window_blue.w, cheats_window_blue.h)
        self.window_type = None

        self.font = pygame.font.Font('font\CookieRun_Regular.ttf', int(FONT_SIZE))
        self.text_list = None
        self.selected = 0
        self.row = 0
        self.col = 0

    def show_window(self, pos, row, col, board):
        self.ShowWindow = True
        self.pos = pos
        self.piece = board[row][col]
        self.row, self.col = row, col
            
        if self.piece.color == 0:
            self.window_type = 1
            self.window = cheats_window_blue_long
            self.items = ["Add Blue", "Add Orange"]
            self.icons = [icon_add, icon_add]
        else:
            if not self.piece.IsKing:
                self.window_type = 3
                self.items = ["Remove", "Promote"]
                self.icons = [icon_remove, icon_promote]
            else:
                self.window_type = 5
                self.items = ["Remove", "Demote"]
                self.icons = [icon_remove, icon_demote]
        
            if self.piece.color == PLAYER_ONE:
                self.window = cheats_window_blue
            else:
                self.window = cheats_window_orange
        
        self.text_list = TextList(font_cookie_run_reg, WHITE, self.items, self.icons, spacing=5, icon_spacing=10, padding=20)
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
                self.selected = i + self.window_type
                pygame.draw.rect(self.surface, BLACK, item_rect)

    def invoke(self):
        match self.selected:
            case 0:
                pass
            case 1:
                print("Added Blue piece")
                # self.add_piece()
            case 2:
                print("Added Orange piece")
                # self.add_piece()
            case 3:
                self.remove()
            case 4:
                self.promote()
            case 5:
                print("Removed piece")
                # self.remove()
            case 6:
                self.demote()  

    def add_piece(self, piece):
        pass

    def remove(self):
        piece = [] 
        piece.append(self.game.board.get_piece(self.row, self.col))
        self.game.board.move_to_graveyard(piece)
        piece.clear()
        print(f"[Cheats]: Removed piece ({self.row}, {self.col})")

    def promote(self):
        piece = self.game.board.get_piece(self.row, self.col).promote()
        print(f"[Cheats]: Promoted piece ({self.row}, {self.col})")

    def demote(self):
        piece = self.game.board.get_piece(self.row, self.col).demote()
        print(f"[Cheats]: Demoted piece ({self.row}, {self.col})")