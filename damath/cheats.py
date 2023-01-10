import pygame
from damath.constants import PLAYER_ONE, PLAYER_TWO
from damath.piece import Piece
from objects import font_cookie_run_reg, cheats_window_blue, icon_add, icon_remove, icon_promote, icon_demote, icon_change_turn, icon_promote_all, icon_demote_all, icon_remove_all, icon_pause_timer, icon_resume_timer
from ui_class.colors import *
from ui_class.textlist import TextList
from ui_class.dropdown_menu import Dropdown
from ui_class.rect_window import RectWindow

FONT_SIZE = cheats_window_blue.h * 0.25
font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(FONT_SIZE))

class Cheats:
    """
    Cheats.
    """
    
    def __init__(self, surface, game):
        self.surface = surface
        self.game = game
        self.pos = ()
        self.items = []
        self.icons = []
        self.ShowWindow = False
        self.TimerIsPaused = False
        
        self.text_box = RectWindow(surface, (0,0), 200, 56, DARK_CERULEAN, 9, 4, WHITE)

        self.font = pygame.font.Font('font\CookieRun_Regular.ttf', int(FONT_SIZE))
        self.text_list = None

        self.piece = Piece(surface, 0, 0, 0, 0)
        self.row = 0
        self.col = 0
        self.selected = None

    def create_window(self, pos, row, col, OnBoard=True):
        self.ShowWindow = True
        self.pos = pos
        self.piece = self.game.board.board[row][col]
        self.row, self.col = row, col
        
        window_color = DARK_CERULEAN

        if OnBoard:
            if self.piece.color == 0:
                self.window_type = 1
                self.items = [" Add Blue", " Add Orange"]
                self.icons = [icon_add, icon_add]
            else:
                if not self.piece.IsKing:
                    self.window_type = 2
                    self.items = [" Remove", " Promote"]
                    self.icons = [icon_remove, icon_promote]
                else:
                    self.window_type = 3
                    self.items = [" Remove", " Demote"]
                    self.icons = [icon_remove, icon_demote]
            
                if self.piece.color == PLAYER_ONE:
                    window_color = DARK_CERULEAN
                    pass
                else:
                    window_color = PERSIMMON_ORANGE
                    pass
        else:
            self.window_type = 0
            self.items = [" Change Turns", " Remove All", " Promote All", " Demote All", " Pause Timer"]
            self.icons = [icon_change_turn, icon_remove_all, icon_promote_all, icon_demote_all, icon_pause_timer]

            if self.TimerIsPaused:
                self.items[4] = " Resume Timer"
                self.icons[4] = icon_resume_timer

        self.text_list = TextList(font_cookie_run_reg, WHITE, self.items, self.icons, spacing=5, icon_spacing=10, padding=[20, 20, 20, 20])
        self.dd = Dropdown(self.surface, self.text_list)
        self.dd.create(pos, color=window_color)

    def draw_menu(self):
        if not self.ShowWindow:
            return

        self.dd.draw()
                
    def invoke(self):
        self.selected = self.dd.get_selected()

        match self.window_type:
            case 0:
                match self.selected:
                    case 0:
                        self.change_turn()
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

    def change_turn(self):
        self.game.change_turn()
        print(f"[Cheats]: Changed turns, now {self.game.turn}")