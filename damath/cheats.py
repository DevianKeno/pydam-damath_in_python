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
        self.piece = Piece(surface, 0, 0, 0, 0)
        self.pos = ()
        self.items = []
        self.icons = []
        self.window_rect = pygame.Rect(0, 0, cheats_window_blue.w, cheats_window_blue.h)
        self.window_type = None
        self.ShowWindow = False

        self.TimerIsPaused = False

        self.font = pygame.font.Font('font\CookieRun_Regular.ttf', int(FONT_SIZE))
        self.text_list = None
        self.selected = None
        self.row = 0
        self.col = 0

    def create_window(self, pos, row, col, OnBoard=True):
        self.ShowWindow = True
        self.pos = pos
        self.piece = self.game.board.board[row][col]
        self.row, self.col = row, col

        if OnBoard:
            if self.piece.color == 0:
                self.window_type = 1
                self.window = cheats_window_blue_long
                self.items = ["Add Blue", "Add Orange"]
                self.icons = [icon_add, icon_add]
            else:
                if not self.piece.IsKing:
                    self.window_type = 2
                    self.items = ["Remove", "Promote"]
                    self.icons = [icon_remove, icon_promote]
                else:
                    self.window_type = 3
                    self.items = ["Remove", "Demote"]
                    self.icons = [icon_remove, icon_demote]
            
                if self.piece.color == PLAYER_ONE:
                    self.window = cheats_window_blue
                else:
                    self.window = cheats_window_orange
        else:
            self.window_type = 0
            self.window = cheats_window_blue_long
            self.items = ["Change Turns", "Remove All", "Promote All", "Demote All", "Pause Timer"]
            self.icons = [icon_add, icon_add, icon_add, icon_add, icon_add]

            if self.TimerIsPaused:
                self.items[4] = "Resume Timer"
                self.icons[4] = icon_add

        self.text_list = TextList(font_cookie_run_reg, WHITE, self.items, self.icons, spacing=5, icon_spacing=10, padding=[20, 20, 20, 20])
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
    
    def check_for_hover(self, m_pos, window_rect):
        for i in range(self.text_list.items_count):
            item_rect = self.text_list.get_rect(i)
            if item_rect.collidepoint(m_pos):
                self.selected = i
                s = pygame.Surface((item_rect.w, item_rect.h))
                s.set_alpha(64)
                s.fill((255, 255, 255))
                self.surface.blit(s, item_rect)
                
                pygame.draw.rect(self.surface, WHITE, item_rect)
            else:
                self.selected = 0
                if window_rect.collidepoint(m_pos):
                    self.selected = None
                    print(self.selected)
                    pygame.draw.rect(self.surface, BLACK, item_rect)

    def invoke(self):
        match self.window_type:
            case 0:
                match self.selected:
                    case 0:
                        print("0")
                        # self.add_piece()
                    case 1:
                        print("1")
                        # self.add_piece()
            case 1:
                match self.selected:
                    case 0:
                        print("Added Blue piece")
                        # self.add_piece()
                    case 1:
                        print("Added Orange piece")
                        # self.add_piece()
            case 2:
                match self.selected:
                    case 0:
                        self.remove()
                    case 1:
                        self.promote()
            case 3:
                match self.selected:
                    case 0:
                        self.remove()
                    case 1:
                        self.demote()  

    def add_piece(self, piece):
        pass

    def remove(self):
        piece = self.game.board.get_piece(self.row, self.col)
        self.game.board.remove(piece)
        print(f"[Cheats]: Removed piece ({self.row}, {self.col})")

    def promote(self):
        self.game.board.get_piece(self.row, self.col).promote()
        print(f"[Cheats]: Promoted piece ({self.row}, {self.col})")

    def demote(self):
        self.game.board.get_piece(self.row, self.col).demote()
        print(f"[Cheats]: Demoted piece ({self.row}, {self.col})")