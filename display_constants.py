import pygame

pygame.init()

reso = pygame.display.Info() # gets the video display information object
SCREEN_WIDTH = 1080 #reso.current_w
SCREEN_HEIGHT = 720 #reso.current_h

BG_COLOR = ((0, 0, 0))

LOGO = pygame.transform.smoothscale(pygame.image.load('assets//icon.png'), (400, 400))
TITLE = pygame.transform.smoothscale(pygame.image.load('assets//title.png'), (820, 265))
