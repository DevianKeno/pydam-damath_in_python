import pygame
from audio_constants import MOVE_SOUND
from damath.constants import PLAYER_ONE, PLAYER_TWO
from damath.piece import Piece
from display_constants import screen
from objects import chips_surface, font_cookie_run_reg, cheats_window_blue, icon_add, icon_remove, icon_promote, icon_demote, icon_change_turn, icon_promote_all, icon_demote_all, icon_remove_all, icon_pause_timer, icon_resume_timer
from options import enableAnimations
from .timer import *
from ui_class.colors import *
from ui_class.font import *
from ui_class.text import Text
from ui_class.text_box import TextBox
from ui_class.textlist import TextList
from ui_class.tween import *
from ui_class.dropdown_menu import Dropdown
from ui_class.rect_window import RectWindow

pygame.mixer.init()

font_size = cheats_window_blue.h * 0.2
font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(font_size))
      
board_centerx = ((screen.get_width()*0.7//2) + (screen.get_width()*0.3)) 
board_centery = screen.get_height()//2 

ev_window_dimensions = (180, 140)
ev_window_radius = 9
ev_window_rect = pygame.Rect((board_centerx-ev_window_dimensions[0]//2, board_centery-ev_window_dimensions[1]//2), (ev_window_dimensions[0], ev_window_dimensions[1]))

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
        self.text_box = RectWindow(surface, (0, 0), 200, 56, DARK_CERULEAN, 9, 4, WHITE)
        self.pos = ()
        self.items = []
        self.icons = []
        self.text_list = None

        self.piece = Piece(surface, (0, 0), 0, 0)
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

        self.dropdown = Dropdown(self.surface, self.text_list)

        """
        "Add Piece" window elements
        """

        self.ev_window = RectWindow(surface, (ev_window_rect.topleft), ev_window_rect.w, ev_window_rect.h, DARK_CERULEAN, ev_window_radius, 4, WHITE)

        self.prompt = Text(surface, CookieRun_Regular, font_size, WHITE)
        self.prompt.text = "Enter Value"
        self.prompt.font_size *= 1.1
        self.prompt.pos = (ev_window_rect.x+ev_window_rect.w//2, ev_window_rect.y+ev_window_rect.h*0.2)
        self.prompt.update()
        
        self.input = Text(surface, CookieRun_Bold, font_size, DARK_CERULEAN)
        self.input.text = '0'
        self.input.font_size *= 1.25
        self.input.update()

        self.text_box_rect = pygame.Rect((board_centerx-ev_text_box_w//2, board_centery-ev_text_box_h//2), (ev_text_box_w, ev_text_box_h))
        self.input_box = TextBox(surface, self.input, self.text_box_rect)
        self.input_box.text = self.input.text

        self.done = Text(surface, CookieRun_Regular, font_size, WHITE)
        self.done.pos = (ev_window_rect.x+ev_window_rect.w//2, ev_window_rect.y+ev_window_rect.h*0.8)
        self.done_hover_area = self.done.text_surface.get_rect(center=(ev_window_rect.x+ev_window_rect.w*0.1, ev_window_rect.y+ev_window_rect.h*0.8), width=ev_window_rect.w*0.8)
        self.done.text = "Done"

    def select(self, cell):
        """
        Selects the cell for invocation purposes.
        """
        
        self.selected_cell = cell
        self.selected_piece = self.game.board.get_piece(self.selected_cell)

    def create_dropdown(self, pos, OnBoard=True):
        """
        Creates the main dropdown menu.
        """
        
        self.ShowMenu = True
        self.pos = pos
        window_color = DARK_CERULEAN
        # self.piece = self.game.board.board[col][row]
        # self.col, self.row = col, row
        

        if OnBoard:
            if self.selected_piece.color == 0:
                self.window_type = 1
                self.items = [" Add Blue", " Add Orange"]
                self.icons = [icon_add, icon_add]
            else:
                if not self.selected_piece.IsKing:
                    self.window_type = 2
                    self.items = [" Remove", " Promote"]
                    self.icons = [icon_remove, icon_promote]
                else:
                    self.window_type = 3
                    self.items = [" Remove", " Demote"]
                    self.icons = [icon_remove, icon_demote]
            
                if self.selected_piece.color == PLAYER_ONE:
                    window_color = DARK_CERULEAN
                    pass
                else:
                    window_color = PERSIMMON_ORANGE
                    pass
        else:
            self.window_type = 0
            self.items = [" Change Turns", " Remove All", " Promote All", " Demote All", " Pause Timer", " Flip Board"]
            self.icons = [icon_change_turn, icon_remove_all, icon_promote_all, icon_demote_all, icon_pause_timer, icon_change_turn]

            if not turn_timer.is_running:
                self.items[4] = " Resume Timer"
                self.icons[4] = icon_resume_timer

        self.text_list = TextList(self.font, WHITE, self.items, self.icons, spacing=5, icon_spacing=10, padding=[20, 20, 20, 20])
        self.dropdown = Dropdown(self.surface, self.text_list)
        self.dropdown.create(pos, color=window_color)
        self.dropdown.IsHoverable = True

    def create_ev_window(self):
        """
        Creates the "Enter Value" window.
        """

        self.ShowEVWindow = True
        self.ev_window.wupdate(x=board_centerx, y=board_centery, width=0, height=0)
        
        self.anim_ev_window = Scale_Rect(self.ev_window, (ev_window_dimensions[0], ev_window_dimensions[1]), 0.2, True, easeOutBack, none, False)
        self.anim_ev_window_inner = Scale_Rect(self.ev_window.inner_rect, (ev_window_dimensions[0]-ev_window_radius//2, ev_window_dimensions[1]-ev_window_radius//2), 0.2, True, easeOutBack, none, False)
        self.anim_ev_window_shadow = Scale_Rect(self.ev_window.shadow_surf_rect, (ev_window_dimensions[0]-ev_window_radius//2, ev_window_dimensions[1]-ev_window_radius//2), 0.2, True, easeOutBack, none, False)
        
    def draw_menu(self):
        if not self.ShowMenu:
            return

        self.dropdown.draw()

        if not self.ShowEVWindow:
            return
        
        self.dropdown.IsHoverable = False
        self.ev_window.draw()

        pygame.draw.rect(self.surface, WHITE, self.text_box_rect, 0, 6)
        self.prompt.draw()
        self.input_box.draw()
        self.done.draw()

        if enableAnimations:
            if self.anim_ev_window.IsFinished:
                return

            self.anim_ev_window.play()
            self.anim_ev_window_inner.play()
            self.anim_ev_window_shadow.play()

    def hide_menus(self, windows=0):
        """
        Hides the menus.

        Args
        0: Hide all.
        1: Hide dropdown menu.
        2: Hide "Enter Value" window.
        """
        match windows:
            case 0:
                self.ShowMenu = False
                self.ShowEVWindow = False
            case 1:
                self.ShowMenu = False
            case 2:
                self.ShowEVWindow = False
        
        self.IsTyping = False

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
        """
        Executes the selected option.
        """
        
        self.selected = self.dropdown.get_selected()

        if self.ShowEVWindow:
            self.add_piece()
            return

        match self.window_type:
            case 0:
                match self.selected:
                    case 0:
                        self.change_turn()
                    case 1:
                        self.remove_all()
                    case 2:
                        self.promote_all()
                    case 3:
                        self.demote_all()
                    case 4:
                        self.toggle_timer()
                    case 5:
                        self.flip_board()
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
        
        self.hide_menus()

    def add_blue(self):
        self.ev_window.change_color(window_color=DARK_CERULEAN)
        self.input.change_color(DARK_CERULEAN) 
        self.add_color = PLAYER_ONE
        self.create_ev_window()

    def add_orange(self):
        self.ev_window.change_color(window_color=PERSIMMON_ORANGE)
        self.input.change_color(BURNT_UMBER) 
        self.add_color = PLAYER_TWO
        self.create_ev_window()

    def add_piece(self):
        MOVE_SOUND.play()
        self.add_value = self.input.text
        piece = Piece(chips_surface, (self.col, self.row), self.add_color, int(self.add_value))
        self.game.board.add_piece(piece)
        self.game.moveable_pieces.append((self.col, self.row))

    def remove(self):
        self.game.board.remove(self.selected_cell)
        print(f"[Cheats]: Removed piece ({self.col}, {self.row})")

    def promote(self):
        self.game.board.get_piece((self.col, self.row)).promote()
        print(f"[Cheats]: Promoted piece ({self.col}, {self.row})")

    def demote(self):
        self.game.board.get_piece((self.col, self.row)).demote()
        print(f"[Cheats]: Demoted piece ({self.col}, {self.row})")

    def change_turn(self):
        self.game.change_turn()
        print(f"[Cheats]: Changed turns, now {self.game.turn}")
        
    def remove_all(self):
        for row in range(8):
            for col in range(8):
                piece = self.game.board.get_piece((col, row))
                self.game.board.remove(piece)
        print(f"[Cheats]: Removed all pieces")

    def promote_all(self):
        for row in range(8):
            for col in range(8):
                self.game.board.get_piece((col, row)).promote()
        print(f"[Cheats]: Promoted all pieces")
        
    def demote_all(self):
        for row in range(8):
            for col in range(8):
                self.game.board.get_piece((col, row)).demote()
        print(f"[Cheats]: Demoted all pieces")

    def toggle_timer(self):
        if self.TimerIsPaused:
            self.TimerIsPaused = False
            turn_timer.resume()
            global_timer.resume()
        else:
            self.TimerIsPaused = True
            turn_timer.pause()
            global_timer.pause()

    def flip_board(self):
        self.game.board.rotate_180()
        self.game.refresh()
        self.game.check_for_captures()