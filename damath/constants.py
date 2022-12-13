import pygame
from ui_class.constants import BTN_COLOR
BOARD_WIDTH = 700
BOARD_HEIGHT = 700  

SCOREBOARD_WIDTH = 225
SCOREBOARD_HEIGHT = 550
SCOREBOARD_COLOR = BTN_COLOR

ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH//COLS

#RGB
RED = '#F93535'
DARKER_RED = '#6D1919'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
BROWN = '#A05B08'
LIGHT_BLUE = '#3B6DFE'
DARKER_BLUE = '#182D69'
YELLOW = '#FFE804'

BLUE_PIECE = pygame.image.load('assets\piece_blue.png')
RED_PIECE = pygame.image.load('assets\piece_red.png')

BLUE_PIECE_KING = pygame.image.load('assets\piece_blue_king.png')
RED_PIECE_KING = pygame.image.load('assets\piece_red_king.png')

BOARD = pygame.transform.smoothscale(pygame.image.load('assets\\vecteezy_chess-board-cropped.jpg'), (BOARD_WIDTH-5, BOARD_HEIGHT-5))

CROWN = pygame.transform.scale(pygame.image.load('assets\crown.png'), (25, 14))
