import pygame
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR

# --------- default values ---------
BTN_COLOR = '#6FB95A'   
TXT_COLOR = 'white'
FONTSIZE = 36

# --------- instantiating Start button ---------
START_BTN_DIMENSION = [250, 65]
START_BTN_POSITION = [SCREEN_WIDTH/2-(START_BTN_DIMENSION[0]/2), (SCREEN_HEIGHT/4)*3]
HOVER_SIZE = 10 # how big the button will grow when hovered