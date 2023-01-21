import pygame
from display_constants import screen
from objects import cheats_window_blue, icon_add
from ui_class.colors import *
from ui_class.dropdown_menu import Dropdown
from ui_class.font import *
from ui_class.text import Text
from ui_class.textlist import TextList
from ui_class.rect_window import RectWindow

font_size = cheats_window_blue.h * 0.2
font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(font_size))

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

    def create_dropdown(self, pos):
        """
        Creates the main dropdown menu.
        """
        
        self.ShowMenu = True
        self.pos = pos
        window_color = DARK_CERULEAN

        self.items = [" Forfeit", " Offer Draw"]
        self.icons = [icon_add, icon_add]

        self.text_list = TextList(self.font, WHITE, self.items, self.icons, spacing=5, icon_spacing=10, padding=[20, 20, 20, 20])
        self.dropdown = Dropdown(self.surface, self.text_list)
        self.dropdown.create(pos, color=window_color)
        self.dropdown.IsHoverable = True

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

        self.hide_menus()

    def draw_menu(self):
        if not self.ShowMenu:
            return
            
        self.dropdown.draw()

    def hide_menus(self):
        """
        Hides the dropdown menu.
        """

        self.ShowMenu = False

    def forfeit(self):
        print("forfeit")
        pass

    def offer_draw(self):
        print("draw")
        pass