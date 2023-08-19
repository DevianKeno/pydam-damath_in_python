import pygame
from console import DeveloperConsole
from damath.constants import PLAYER_ONE, PLAYER_TWO
from damath.game import Match
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

    def __init__(self) -> None:
        self._surface = None
        self._console = None
        self._game = None

        self.font = font_cookie_run_reg
        self.items = []
        self.icons = []
        self.text_list = None
        self.dropdown = Dropdown(self._surface, self.text_list)
        self.ShowDropdown = False

    @property
    def Surface(self):
        return self._surface

    @Surface.setter
    def Surface(self, surface: pygame.Surface):
        self._surface = surface

    @property
    def Console(self):
        return self._console

    @Console.setter
    def Console(self, console: DeveloperConsole):
        self._console = console

    @property
    def Game(self):
        return self._game

    @Game.setter
    def Game(self, value: Match):
        self._game = value

    def init(self):

        # "Forfeit?" Window
        self.ShowFFWindow = False
        self.confirmation_window = RectWindow(self._surface,
                                    (ff_window_rect.topleft), 
                                    ff_window_rect.w, ff_window_rect.h, 
                                    DARK_CERULEAN, ff_window_radius, 4, WHITE)

        self.prompt = Text(self._surface, CookieRun_Regular, font_size, WHITE)
        self.prompt.font_size *= 1.5
        self.prompt.pos = (ff_window_rect.x+ff_window_rect.w//2, ff_window_rect.y+ff_window_rect.h*0.3)

        self.button_ff_yes = NButton(self._surface, pos=((ff_window_rect.x - button_default_w//2) + ff_window_rect.w*0.3, (ff_window_rect.y + ff_window_rect.h*0.66) - button_default_h//2),
                                     width=button_default_w, height=button_default_h,
                                     text="Yes",
                                     rect_color=(200, 56, 67),
                                     shadow_rect_color=(123, 3, 11),
                                     target=self._ffyes)
        self.button_no = NButton(self._surface, pos=((ff_window_rect.x - button_default_w//2) + ff_window_rect.w*0.7, (ff_window_rect.y + ff_window_rect.h*0.66) - button_default_h//2),
                                    width=button_default_w, height=button_default_h,
                                    text="No",
                                    target=self._ffno)

        # "Offer Draw?" Window
        self.ShowODWindow = False
        self.button_od_yes = NButton(self._surface, pos=((ff_window_rect.x - button_default_w//2) + ff_window_rect.w*0.3, (ff_window_rect.y + ff_window_rect.h*0.66) - button_default_h//2),
                                     width=button_default_w, height=button_default_h,
                                     text="Yes",
                                     rect_color=(231, 126, 48),
                                     shadow_rect_color=(148, 58, 12),
                                     target=self._odyes)
    
    def set_surface(self, surface: pygame.Surface):
        self._surface = surface

    def create_dropdown(self, pos):
        """
        Creates the main dropdown menu.
        """
        
        window_color = DARK_CERULEAN
        self.ShowDropdown = True
        self.pos = pos
        x = pos[0]
        y = pos[1]

        if self._game.turn == PLAYER_ONE:
            window_color = DARK_CERULEAN
        else:
            window_color = PERSIMMON_ORANGE

        self.items = [" Forfeit", " Offer Draw"]
        self.icons = [icon_forfeit, icon_offer_draw]

        self.text_list = TextList(self.font, WHITE, self.items, self.icons, spacing=5, icon_spacing=10, padding=[20, 20, 20, 20])
        self.dropdown = Dropdown(self._surface, self.text_list)
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
        self.prompt.text = "Forfeit?"
        self.prompt.update()

    def create_od_window(self):
        """
        Creates the "Offer Draw?" window.
        """
        self.ShowODWindow = True
        self.prompt.text = "Offer Draw?"
        self.prompt.update()
        
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

    def draw_menu(self):
        if not self.ShowDropdown:
            return

        self.dropdown.draw()

        if self.ShowFFWindow:
            self.draw_ff()

        if self.ShowODWindow:
            self.draw_od()

    def draw_ff(self):
        self.dropdown.IsHoverable = False
        self.confirmation_window.draw()
        self.prompt.draw()
        self.button_ff_yes.draw()
        self.button_no.draw()

    def draw_od(self):
        self.dropdown.IsHoverable = False
        self.confirmation_window.draw()
        self.prompt.draw()
        self.button_od_yes.draw()
        self.button_no.draw()
            
    def hide_menus(self, windows=0):
        """
        Hides the menus.

        Args
        0: Hide all.
        1: Hide dropdown menu.
        2: Hide "Forfeit" window.
        3: Hide "Offer Draw?" window.
        """
        match windows:
            case 0:
                self.ShowDropdown = False
                self.ShowFFWindow = False
                self.ShowODWindow = False
            case 1:
                self.ShowDropdown = False
            case 2:
                self.ShowFFWindow = False
            case 3:
                self.ShowODWindow = False

    def forfeit(self):
        self.create_ff_window()

    def _ffyes(self):
        self._console._command_ffyes()
        self.hide_menus()

    def _ffno(self):
        self.hide_menus()

    def offer_draw(self):
        self.create_od_window()

    def _odyes(self):
        self._console._command_drawyes()
        self.hide_menus()

    def _odno(self):
        self.hide_menus()