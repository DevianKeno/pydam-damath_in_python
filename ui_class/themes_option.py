import pygame
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from audio_constants import SWIPE_SOUND

class ThemesList:

    def __init__(self, screen):
        self.screen = screen
        self.list = []
        self.rect_list = []
        self.focused = 0

    def append(self, Theme):
        self.list.append(Theme)        
        self.rect_append(None)

    def rect_append(self, Rect):
        self.rect_list.append(Rect)

    def print(self):
        return print(self.list)

    def display(self):

        for idx, theme in enumerate(self.list):

            #pygame.draw.rect(self.screen, WHITE, self.rect_list[idx])
            if theme.x == SCREEN_WIDTH//2 - theme.theme.get_width()//2:
                theme.theme.set_alpha(255)
                theme.bg.set_alpha(50)
                self.screen.blit(theme.bg, (SCREEN_WIDTH//2-theme.bg.get_width()//2, SCREEN_HEIGHT//2-theme.bg.get_height()//2))
                self.screen.blit(theme.theme, (theme.x, theme.y))
                self.focused = theme.number                
            else:
                theme.theme.set_alpha(100)
                self.screen.blit(theme.theme, (theme.x, theme.y))

    def move(self, direction):

        for theme in self.list:
            if theme.x == SCREEN_WIDTH//2 - theme.theme.get_width()//2:
                theme.theme.set_alpha(255)
                theme.bg.set_alpha(50)
                self.screen.blit(theme.bg, (SCREEN_WIDTH//2-theme.bg.get_width()//2, SCREEN_HEIGHT//2-theme.bg.get_height()//2))
                self.screen.blit(theme.theme, (theme.x, theme.y))
                self.focused = theme.number                
            else:
                theme.theme.set_alpha(100)
                self.screen.blit(theme.theme, (theme.x, theme.y))

            if direction == 'left':
                if self.focused == len(self.list)-1:
                    break
                theme.move_left()
            else:
                if self.focused == 0:
                    break
                theme.move_right()


        
# --------- Themes class ---------
class Themes:

    SPEED = 5

    def __init__(self, screen, theme, number):
        self.screen = screen
        self.selected = False
        self.number = number
        
        self.board = theme
        
        self.bg = pygame.transform.smoothscale(theme, (600, 600))
        self.theme = pygame.transform.smoothscale(theme, (300, 300))
        
        self.x = SCREEN_WIDTH//2 - self.theme.get_width()//2
        self.y = SCREEN_HEIGHT//2 - self.theme.get_height()//2
        self.gap = SCREEN_WIDTH//2 - self.theme.get_width()//2

        if self.number > 0:
            for _ in range(number):
                self.x += self.gap

    def move_left(self):
        SWIPE_SOUND.set_volume(0.2)
        SWIPE_SOUND.play()
        target = self.x - self.gap

        while target != self.x:
            self.x -= self.SPEED
            self.screen.blit(self.theme, (self.x, self.y))


    def move_right(self):
        SWIPE_SOUND.set_volume(0.2)
        SWIPE_SOUND.play()
        target = self.x + self.gap
        while target != self.x:
            self.x += self.SPEED
            self.screen.blit(self.theme, (self.x, self.y))
                
