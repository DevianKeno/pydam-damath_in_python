import pygame

pygame.init()

reso = pygame.display.Info() # gets the video display information object
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

LOGO_png = pygame.transform.smoothscale(pygame.image.load('assets//icon.png'), (400, 400))
