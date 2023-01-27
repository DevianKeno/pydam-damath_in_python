import pygame
import sys
from display_constants import FPS
from event_loop import event_loop
from objects import CURSOR
from ui_class.colors import OAR_BLUE

clock = pygame.time.Clock()
class Screen:
    
    def __init__(self, screen: pygame.Surface, bg_color=OAR_BLUE, bg_music=None, on_loop: bool=True, target=None):

        self.screen = screen
        self.bg_color = bg_color

        self.bg_music = bg_music
        self.on_loop = on_loop
        self.music_playing = False
        self.running = False
        self.target = target

    def play_music(self): 
        
        pygame.mixer_music.stop()

        if self.bg_music != None:
            pygame.mixer_music.load()
            if self.on_loop:
                pygame.mixer_music.play(-1)
            else:
                pygame.mixer_music.play()
            
            self.music_playing = True

    def before_looping(self):
        """
        Override this function with the code that you
        want to execute BEFORE the loop starts
        """

        if not self.music_playing:
            self.play_music()

    def while_looping(self):
        """
        Override this function with the code that you
        want to execute WHILE on loop
        """        

        self.screen.blit(CURSOR, pygame.mouse.get_pos())

    def after_looping(self):
        """
        Override this function with the code that you
        want to execute AFTER the loop finishes
        """
        print("stopped")

    def start(self):

        self.before_looping()
        self.running = True
        
        while self.running:
            self.while_looping()
            self.event_loop()
            self.update()

        self.after_looping()

    def event_loop(self):
        for event in event_loop.get_event():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()    

    def update(self):
        pygame.display.update()
        clock.tick(FPS)

    def reset(self):
        self.running = False