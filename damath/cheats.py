import pygame
from damath.constants import PLAYER_ONE, PLAYER_TWO
from damath.piece import Piece
from objects import chips_surface, font_cookie_run_reg, cheats_window_blue, icon_add, icon_remove, icon_promote, icon_demote, icon_change_turn, icon_promote_all, icon_demote_all, icon_remove_all, icon_pause_timer, icon_resume_timer
from ui_class.colors import *
from ui_class.font import *
from ui_class.text import Text
from ui_class.text_box import TextBox
from ui_class.textlist import TextList
from ui_class.dropdown_menu import Dropdown
from ui_class.rect_window import RectWindow

font_size = cheats_window_blue.h * 0.2
font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(font_size))

ev_window_w = 180
ev_window_h = 140
ev_text_box_w = 120
ev_text_box_h = 36

class Cheats:
    """
    Cheats.
    """
    
    def __init__(self, surface, game):
        self.surface = surface
        self.game = game

        self.font = font_cookie_run_reg
        self.text_box = RectWindow(surface, (0,0), 200, 56, DARK_CERULEAN, 9, 4, WHITE)
        self.pos = ()
        self.items = []
        self.icons = []
        self.text_list = None

        self.piece = Piece(surface, 0, 0, 0, 0)
        self.row = 0
        self.col = 0
        self.selected = None
        self.selected_done = 0
        self.add_value = '0'
        self.add_color = None
        
        self.ShowMenu = False
        self.ShowEVWindow = False
        self.TimerIsPaused = False
        self.IsTyping = False

        self.dd = Dropdown(self.surface, self.text_list)

        self.board_mid_x = ((surface.get_width()*0.7//2) + (surface.get_width()*0.3)) 
        self.board_mid_y = surface.get_height()//2 

        # Add piece window elements
        self.ev_window = RectWindow(surface, (self.board_mid_x-ev_window_w//2, self.board_mid_y-ev_window_h//2), ev_window_w, ev_window_h, DARK_CERULEAN, 9, 4, WHITE)
        
        self.prompt = Text(surface, CookieRun_Regular, font_size, WHITE)
        self.prompt.text = "Enter Value"
        self.prompt.font_size *= 1.1
        self.prompt.pos = (self.ev_window.x+self.ev_window.w//2, self.ev_window.y+self.ev_window.h*0.2)
        self.prompt.update()
        
        self.input = Text(surface, CookieRun_Bold, font_size, DARK_CERULEAN)
        self.input.text = '0'
        self.input.font_size *= 1.25
        self.input.update()

        self.text_box_rect = pygame.Rect((self.board_mid_x-ev_text_box_w//2, self.board_mid_y-ev_text_box_h//2), (ev_text_box_w, ev_text_box_h))
        self.input_box = TextBox(surface, self.input, self.text_box_rect)
        self.input_box.text = self.input.text

        self.done = Text(surface, CookieRun_Regular, font_size, WHITE)
        self.done.pos = (self.ev_window.x+self.ev_window.w//2, self.ev_window.y+self.ev_window.h*0.8)
        self.done_hover_area = self.done.text_surface.get_rect(center=(self.ev_window.x+self.ev_window.w*0.1, self.ev_window.y+self.ev_window.h*0.8), width=self.ev_window.w*0.8)
        self.done.text = "Done"

    def create_window(self, pos, row, col, OnBoard=True):
        self.ShowMenu = True
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

        self.text_list = TextList(self.font, WHITE, self.items, self.icons, spacing=5, icon_spacing=10, padding=[20, 20, 20, 20])
        self.dd = Dropdown(self.surface, self.text_list)
        self.dd.create(pos, color=window_color)

    def draw_menu(self):
        if not self.ShowMenu:
            return

        self.dd.draw()

        if not self.ShowEVWindow:
            return
        
        self.ev_window.draw()
        pygame.draw.rect(self.surface, WHITE, self.text_box_rect, 0, 6)
        self.prompt.draw()
        self.input_box.draw()
        self.done.draw()

    def hide_menus(self, windows=0):
        match windows:
            case 0:
                self.ShowMenu = False
                self.ShowEVWindow = False
            case 1:
                self.ShowMenu = False
            case 2:
                self.ShowEVWindow = False

    def check_for_hover(self, m_pos):
        if self.done_hover_area.collidepoint(m_pos):
            self.selected_done = 1
            hover_area = pygame.Surface((self.done_hover_area.w, self.done_hover_area.h))
            hover_area.set_alpha(64)
            hover_area.fill((255, 255, 255))
            self.surface.blit(hover_area, self.done_hover_area)
        else:
            self.selected_done = 0

    def invoke(self):
        self.selected = self.dd.get_selected()

        if self.ShowEVWindow:
            self.add_piece()
            return

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
                        self.add_blue()
                    case 1:
                        self.add_orange()
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

    def add_blue(self):
        self.ev_window.change_color(window_color=DARK_CERULEAN)
        self.input.change_color(DARK_CERULEAN) 
        self.ShowEVWindow = True
        self.add_color = PLAYER_ONE

    def add_orange(self):
        self.ev_window.change_color(window_color=PERSIMMON_ORANGE)
        self.input.change_color(BURNT_UMBER) 
        self.ShowEVWindow = True
        self.add_color = PLAYER_TWO

    def add_piece(self):
        self.add_value = self.input.text
        piece = Piece(chips_surface, self.row, self.col, self.add_color, int(self.add_value))
        self.game.board.add_piece(piece)
        self.game.moveable_pieces.append((self.row, self.col))

    def remove(self):
        piece = self.game.board.get_piece(self.row, self.col)
        self.game.board.remove(piece)
        print(f"[Cheats]: Removed piece ({self.row}, {self.col})")
        self.hide_menus()

    def promote(self):
        self.game.board.get_piece(self.row, self.col).promote()
        print(f"[Cheats]: Promoted piece ({self.row}, {self.col})")
        self.hide_menus()

    def demote(self):
        self.game.board.get_piece(self.row, self.col).demote()
        print(f"[Cheats]: Demoted piece ({self.row}, {self.col})")
        self.hide_menus()

    def change_turn(self):
        self.game.change_turn()
        print(f"[Cheats]: Changed turns, now {self.game.turn}")
        self.hide_menus()