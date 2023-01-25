import pygame
from damath.constants import PLAYER_ONE, PLAYER_TWO
from display_constants import screen
from objects import cheats_window_blue, icon_forfeit, icon_offer_draw
from ui_class.colors import *
from ui_class.dropdown_menu import Dropdown
from ui_class.font import *
from ui_class.text import Text
from ui_class.textlist import TextList
from ui_class.rect_window import RectWindow
from ui_class.new_btn import NButton

font_size = cheats_window_blue.h * 0.2
font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(font_size))

screen_w = screen.get_width()
screen_h = screen.get_height()
screen_centerx = screen.get_width() // 2
screen_centery = screen.get_height() // 2

ff_window_dims = screen_w * 0.25, screen_h * 0.175
ff_window_radius = 9
ff_window_rect = pygame.Rect((screen_centerx-ff_window_dims[0]//2, screen_centery-ff_window_dims[1]//2), (ff_window_dims[0], ff_window_dims[1]))

button_default_w = 150
button_default_h = 50

class Actions:

    def __init__(self, surface, game) -> None:
        self.surface = surface
        self.game = game

        self.font = font_cookie_run_reg
        self.items = []
        self.icons = []
        self.text_list = None
        self.dropdown = Dropdown(self.surface, self.text_list)
        
        self.ShowMenu = False

        # "Forfeit?" Window
        self.ShowFFWindow = False
        self.ff_window = RectWindow(surface,
                                    (ff_window_rect.topleft), 
                                    ff_window_rect.w, ff_window_rect.h, 
                                    DARK_CERULEAN, ff_window_radius, 4, WHITE)

        self.prompt = Text(surface, CookieRun_Regular, font_size, WHITE)
        self.prompt.text = "Forfeit?"
        self.prompt.font_size *= 1.5
        self.prompt.pos = (ff_window_rect.x+ff_window_rect.w//2, ff_window_rect.y+ff_window_rect.h*0.3)
        self.prompt.update()

        self.button_ff_yes = NButton(surface, pos=((ff_window_rect.x - button_default_w//2) + ff_window_rect.w*0.3, (ff_window_rect.y + ff_window_rect.h*0.66) - button_default_h//2),
                                     width=button_default_w, height=button_default_h,
                                     text="Yes",
                                     rect_color=(200, 56, 67),
                                     shadow_rect_color=(123, 3, 11))
        self.button_ff_no = NButton(surface, pos=((ff_window_rect.x - button_default_w//2) + ff_window_rect.w*0.7, (ff_window_rect.y + ff_window_rect.h*0.66) - button_default_h//2),
                                    width=button_default_w, height=button_default_h,
                                    text="No")

    def create_dropdown(self, pos):
        """
        Creates the main dropdown menu.
        """
        
        window_color = DARK_CERULEAN
        self.ShowMenu = True
        self.pos = pos
        x = pos[0]
        y = pos[1]

        if self.game.turn == PLAYER_ONE:
            window_color = DARK_CERULEAN
        else:
            window_color = PERSIMMON_ORANGE

        self.items = [" Forfeit", " Offer Draw"]
        self.icons = [icon_forfeit, icon_offer_draw]

        self.text_list = TextList(self.font, WHITE, self.items, self.icons, spacing=5, icon_spacing=10, padding=[20, 20, 20, 20])
        self.dropdown = Dropdown(self.surface, self.text_list)
        self.dropdown.create(pos, color=window_color)

        # Screen cropping
        if x > (screen.get_width() - self.dropdown.window.w):
            x = x - self.dropdown.window.w
        if y > (screen.get_height() - self.dropdown.window.h):
            y = y - self.dropdown.window.h
        pos = x, y
        
        self.dropdown.move_to(pos)
        self.dropdown.IsHoverable = True

    def create_ff_window(self):
        """
        Creates the "Forfeit?" window.
        """
        self.ShowFFWindow = True
        
    def invoke(self):
        """
        Executes the selected option.
        """

        self.selected = self.dropdown.get_selected()

        match self.selected:
            case 0:
                self.forfeit()
            case 1:
                self.offer_draw()

        # self.hide_menus()

    def draw_menu(self):
        if not self.ShowMenu:
            return

        self.dropdown.draw()

        if not self.ShowFFWindow:
            return

        self.dropdown.IsHoverable = False
        self.ff_window.draw()
        self.prompt.draw()
        self.button_ff_yes.draw()
        self.button_ff_no.draw()
            
    def hide_menus(self, windows=0):
        """
        Hides the menus.

        Args
        0: Hide all.
        1: Hide dropdown menu.
        2: Hide "Forfeit" window.
        """
        match windows:
            case 0:
                self.ShowMenu = False
                self.ShowFFWindow = False
            case 1:
                self.ShowMenu = False
            case 2:
                self.ShowFFWindow = False

    def forfeit(self):
        print("forfeit")
        self.create_ff_window()
        pass

    def offer_draw(self):
        print("draw")
        pass