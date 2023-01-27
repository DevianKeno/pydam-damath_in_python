import pygame
from display_constants import SCREEN_WIDTH, SIDE_MENU_RECT_CURRENT, SIDE_MENU_RECT_ACTIVE
from objects import screen_copy, sidebar, LOGO
from ui_class.fade_anim import Fade
from .screen import Screen
from .sidebar_display import *

class MainMenuScreen(Screen):
    def __init__(self, screen: pygame.Surface, bg_color, bg_music=None, on_loop: bool = True, target=None):
        super().__init__(screen, bg_color, bg_music, on_loop, target)

        self.move_title = False
        self.font = pygame.font.Font('font\CookieRun_Bold.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05)) 
        self.fade_screen = Fade(screen, screen_copy, pygame.Color(OAR_BLUE), (SIDE_MENU_RECT_CURRENT.width + (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/11, 0), speed=25)
        self._text = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def main_screen(self):
        return SCREEN_WIDTH - sidebar.sidebar_rect.w

    def before_looping(self):

        self.text_option = self.font.render(str(self.text), True, WHITE)

        self.fade_screen.reset()
        if anim_title_upper.IsFinished:
            anim_title_down.play()
        else:
            anim_title_down.IsFinished = True
            anim_title_up.play()
        
        super().before_looping()

    def while_looping(self):

        if self.move_title:
            try:
                title_upper(self.window_function)
            except:
                pass
        else:
            if anim_title_upper.IsFinished:
                anim_title_down.play()
                if anim_title_down.IsFinished:
                    anim_title_upper.reset()

        sidebar.display(self.target)
        self.screen.blit(LOGO, (sidebar.sidebar_rect.width/2 - LOGO.get_width()/2, side_menu_surface.get_height()*0.075))
        self.fade_screen.change_pos((sidebar.sidebar_rect.width, 0))
        title_up_display(self.fade_screen)

        if self.fade_screen.finished:
            self.screen.blit(self.text_option, (sidebar.sidebar_rect.width + 
                        self.main_screen/11, title.y+TITLE.get_height()*1.15))

        super().while_looping()

    def reset(self):
        self.fade_screen.reset()
        self.move_title = False
        return super().reset()