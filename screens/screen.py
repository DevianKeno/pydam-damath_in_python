import pygame
import sys
from abc import *
from typing import Type, BinaryIO
from display_constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, screen
from event_loop import event_loop
from objects import CURSOR
from ui_class.colors import OAR_BLUE

width = int
height = int
class Screen(ABC):

    clock = pygame.time.Clock()

    def __init__(self, bg_color, bg_music: BinaryIO):

        self.screen = screen
        self.bg_color = bg_color
        self.bg_music = bg_music

        self.music_playing = False
        self.running = False

    @property
    def size(self) -> tuple[width, height]:
        return tuple(self.screen.get_size())

    @property
    def width(self) -> width:
        return self.screen.get_width()

    @property
    def height(self) -> height:
        return self.screen.get_height()

    @property
    def mouse_pos(self) -> tuple:
        return pygame.mouse.get_pos()

    @property
    def mx(self) -> int:
        return self.mouse_pos[0]

    @property
    def my(self) -> int:
        return self.mouse_pos[1]

    @abstractmethod
    def before_looping(self):
        """
        Override this function with the code that you
        want to execute BEFORE the loop starts
        """

    @abstractmethod
    def while_looping(self):
        """
        Place here the order of layers you want to display while looping
        (e.g. fill() -> draw_something() -> do_something() -> show_cursor())

        check_event() and update() will automatically be called 
        after all the codes here has been executed
        """

    # @abstractmethod
    def after_looping(self):
        """
        Override this function with the code that you
        want to execute AFTER the loop finishes
        """

    def fill(self):
        """
        Fills the screen with the passed bg color,

        It will automatically be called at the very start of the loop
        before calling while_looping()
        """
        self.screen.fill(self.bg_color)

    def play_music(self): 
        """
        Stops any music that is currently playing if there's any,
        and play the passed bg_music on loop
        """
        pygame.mixer_music.stop()

        if self.bg_music != None:
            pygame.mixer_music.load(self.bg_music)
            pygame.mixer_music.play(-1)

            self.music_playing = True

    def display_cursor(self):
        """
        It basically displays the cursor to the screen,

        It will automatically be called after get_events
        """
        self.screen.blit(CURSOR, pygame.mouse.get_pos())

    def get_events(self):
        """
        Event loop.

        This automatically gets called after
        executing while_looping()
        """
        for event in event_loop.get_event():
        # for event in event_loop.event_list:
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()    

    def update(self):
        """
        Updates the whole display.

        This automatically gets called 
        after executing display_cursor()
        """
        pygame.display.update()
        self.clock.tick(FPS)
    
    def display(self):
        """
        Starts the loop
        """
        self.play_music()
        self.before_looping()
        self.running = True
        
        while self.running:
            self.fill()
            self.while_looping()
            self.get_events()
            self.display_cursor()
            self.update()

        self.after_looping()

    def stop(self):
        """
        Stops the loop.
        """
        self.running = False

