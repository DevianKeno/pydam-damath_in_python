import pygame

pygame.init()

reso = pygame.display.Info() # gets the video display information object
SCREEN_WIDTH =  reso.current_w 
SCREEN_HEIGHT =  reso.current_h 
#SCREEN_WIDTH = 1080
#SCREEN_HEIGHT = 720
BG_COLOR = ('#627E9B') # lighter shade of blue

SIDE_MENU_COLOR = ('#2C455E') # darker shade of blue
SIDE_MENU_RECT = pygame.Rect(0, 0, SCREEN_WIDTH*0.29, SCREEN_HEIGHT) #(313, 720)

TITLE_BG = pygame.transform.smoothscale(pygame.image.load('assets//title_bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
CLEAR_BG = pygame.transform.smoothscale(pygame.image.load('assets//CLEAR_BG.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
LOGO = pygame.transform.smoothscale(pygame.image.load('new_assets/logo.png'), (225, 225))
TITLE = pygame.transform.smoothscale(pygame.image.load('assets//title.png'), (650, 210))
