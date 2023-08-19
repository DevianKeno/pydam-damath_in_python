from __future__ import annotations
import pygame
from .screen import Screen
from display_constants import SCREEN_WIDTH, SIDE_MENU_RECT_CURRENT, SIDE_MENU_RECT_ACTIVE
from objects import screen, screen_copy, sidebar, title_surface, side_menu_surface, \
            anim_title_slide_down, anim_title_slide_up, anim_title_slide_past_screen,  \
            title, TITLE, LOGO
from ui_class.fade_anim import Fade
from ui_class.colors import OAR_BLUE, WHITE
from scenes.title_scene import TitleScene

class MainMenu(Screen):

    font = pygame.font.Font('font\CookieRun_Bold.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05)) 
    fade_screen = Fade(screen, screen_copy, pygame.Color(OAR_BLUE), (SIDE_MENU_RECT_CURRENT.width + (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/11, 0), speed=25)
    
    def __init__(self, bg_color, bg_music):
        super().__init__(bg_color, bg_music)

        self.title_moved = False       # checks if the TITLE has moved above the screen
        self._name = None         # stores the name of the main menu


    @property
    def name(self) -> name:
        return self._name

    @name.setter
    def text(self, name):
        self._name = name

    @property
    def main_screen(self) -> int:
        """
        Returns the current size of the main screen disregarding the sidebar 
        """
        return SCREEN_WIDTH - sidebar.sidebar_rect.w

    @classmethod
    def reset(cls):
        cls.fade_screen.reset()
        cls.title_moved = False

    @staticmethod
    def title_slide_up(fade_screen):
        """
        For moving the title img up + fade animation 
        """

        title_surface.fill(OAR_BLUE)
        title_surface.set_colorkey(OAR_BLUE)
        
        anim_title_slide_up.play()

        if anim_title_slide_up.IsFinished:
            fade_screen.full_fade() 

        title.display()

        screen.blit(title_surface, (((SCREEN_WIDTH-sidebar.sidebar_rect.w)//2)+
                sidebar.sidebar_rect.w-title_surface.get_width()//2, 0))

        fade_screen.change_pos((sidebar.sidebar_rect.width, 0))

    @staticmethod
    def title_slide_above_screen():

        if anim_title_slide_down.IsFinished:
            anim_title_slide_past_screen.play()
            if anim_title_slide_past_screen.IsFinished:
                anim_title_slide_down.reset()

    @staticmethod
    def call_target(func: callable):
        if anim_title_slide_past_screen.IsFinished:
            func()

    @staticmethod
    def reset_title_position():
        """
        Slide down if the title is past the screen, and reset
        """
        if anim_title_slide_past_screen.IsFinished:
            anim_title_slide_down.play()
            if anim_title_slide_down.IsFinished:
                anim_title_slide_past_screen.reset()

    @staticmethod
    def display_logo():
        """
        Displays the LOGO image on the sidebar
        """
        screen.blit(LOGO, (sidebar.sidebar_rect.width/2 - LOGO.get_width()/2, side_menu_surface.get_height()*0.075))    

    @staticmethod
    def display_sidebar(func):
        """
        Displays the sidebar
        """
        sidebar.display(func)

    def display_mode_name(self):
        self.screen.blit(self.text_option, (sidebar.sidebar_rect.width + 
                    self.main_screen/11, title.y+TITLE.get_height()*1.15))

    def initialize(self):
        """
        Checks some variables, resets, and renders the text option to be displayed
        """

        # self.reset()
        self.text_option = self.font.render(str(self.text), True, WHITE)

        if anim_title_slide_past_screen.IsFinished:
            anim_title_slide_down.play()
        else:
            anim_title_slide_down.IsFinished = True
            anim_title_slide_up.play()

        if not pygame.mixer_music.get_busy():
            pygame.mixer_music.load("audio\DamPy.wav")
            pygame.mixer_music.play(-1)