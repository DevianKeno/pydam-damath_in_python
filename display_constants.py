import pygame

pygame.init()

reso = pygame.display.Info() # gets the video display information object

SCREEN_WIDTH =  reso.current_w 
SCREEN_HEIGHT =  reso.current_h 
#SCREEN_WIDTH = 1368
#SCREEN_HEIGHT = 768
BG_COLOR = ('#627E9B') # lighter shade of blue
MAIN_TXT_COLOR = ('#7697B9')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dampy') # window caption
LOGO = pygame.transform.smoothscale(pygame.image.load('new_assets/logo.png'), (SCREEN_WIDTH*0.1285, SCREEN_WIDTH*0.1285))
pygame.display.set_icon(LOGO)

SIDE_MENU_COLOR = ('#2C455E') # darker shade of blue
SIDE_MENU_RECT = pygame.Rect(0, 0, SCREEN_WIDTH*0.3, SCREEN_HEIGHT) #(313, 720) original = 0.29

TITLE = pygame.transform.smoothscale(pygame.image.load('assets//title.png'), (SCREEN_WIDTH*0.65, SCREEN_HEIGHT*0.65))
TITLE_BG = pygame.transform.smoothscale(pygame.image.load('assets//title_bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
CLEAR_BG = pygame.transform.smoothscale(pygame.image.load('assets//CLEAR_BG.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))