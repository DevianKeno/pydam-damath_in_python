import pygame
import numpy as np

pygame.init()
reso = pygame.display.Info() # gets the video display information object

# SCREEN_WIDTH =  reso.current_w 
# SCREEN_HEIGHT =  reso.current_h 

# dict for all supported resolutions in the game
SUPPORTED_RESO = {
    854:480,
    1024:576,
    1280:720,
    1366:768,
    1600:900,
    1920:1080    
}

if SUPPORTED_RESO.get(reso.current_w) == None or SUPPORTED_RESO.get(reso.current_w != reso.current_h):
    """
    if the current resolution is not supported
    """
    resolutions = []
    reso_keys = [key for key in SUPPORTED_RESO.keys()]
    
    # get the difference of all the supported widths and the current width
    for key in reso_keys:
        diff = reso.current_w - key
        if diff > 0: resolutions.append(diff)
        else: resolutions.append(key)

    # get the least difference in the list (closest resolution lower than the current one)
    idx = np.argmin(resolutions)

    SCREEN_WIDTH = reso_keys[idx]
    SCREEN_HEIGHT = SUPPORTED_RESO.get(SCREEN_WIDTH)
else:
    SCREEN_WIDTH =  reso.current_h
    SCREEN_HEIGHT =  reso.current_w

print(F'[Current Resolution]: {SCREEN_WIDTH} x {SCREEN_HEIGHT}')
FPS = 60

BG_COLOR = ('#627E9B') # lighter shade of blue
MAIN_TXT_COLOR = ('#7697B9')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dampy') # window caption
LOGO = pygame.transform.smoothscale(pygame.image.load('new_assets/logo.png'), (SCREEN_WIDTH*0.12, SCREEN_WIDTH*0.12))
pygame.display.set_icon(LOGO)

SIDE_MENU_COLOR = ('#2C455E') # darker shade of blue
SIDE_MENU_RECT_ACTIVE = pygame.Rect(0, 0, SCREEN_WIDTH*0.3, SCREEN_HEIGHT) #(313, 720) original = 0.29
SIDE_MENU_RECT_DEFAULT = pygame.Rect(0, 0, SCREEN_WIDTH*0.15, SCREEN_HEIGHT)
SIDE_MENU_RECT_CURRENT = pygame.Rect(0, 0, SCREEN_WIDTH*0.15, SCREEN_HEIGHT)

TITLE = pygame.image.load('assets/title.png').convert_alpha()
TITLE_SIZE = (0.65, 0.65)

TEST = pygame.image.load('assets/piece_blue.png').convert_alpha()

TITLE_BG = pygame.transform.smoothscale(pygame.image.load('assets//title_bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
CLEAR_BG = pygame.transform.smoothscale(pygame.image.load('assets//CLEAR_BG.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))