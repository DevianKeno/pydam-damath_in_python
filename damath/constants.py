import pygame
from ui_class.constants import BTN_COLOR

BOARD_WIDTH = 620
BOARD_HEIGHT = 620  

SCOREBOARD_WIDTH = 245
SCOREBOARD_HEIGHT = 495
SCOREBOARD_COLOR = BTN_COLOR
SCOREBOARD_ALPHA = 180

SCOREBOARD_RED = pygame.transform.smoothscale(pygame.image.load('assets\SCOREBOARD_RED.png'), (250, 250))
SCOREBOARD_BLUE = pygame.transform.smoothscale(pygame.image.load('assets\SCOREBOARD_BLUE.png'), (250, 250))
SCOREBOARD_RED_ACTIVE = pygame.transform.smoothscale(pygame.image.load('assets\SCOREBOARD_RED_ACTIVE.png'), (250, 250))
SCOREBOARD_BLUE_ACTIVE = pygame.transform.smoothscale(pygame.image.load('assets\SCOREBOARD_BLUE_ACTIVE.png'), (250, 250))

ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH//COLS

OFFSET = 33
BOARD_OFFSET = 58

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

#BOARD_1 = pygame.transform.smoothscale(pygame.image.load('assets\\vecteezy_chess-board-cropped.jpg'), (BOARD_WIDTH-5, BOARD_HEIGHT-5))
BOARD_BLACK = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_BLACK.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))
BOARD_BROWN = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_BROWN.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))
BOARD_GREEN = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_GREEN.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))
BOARD_LIGHTBROWN = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_LIGHTBROWN.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))
BOARD_BLUE = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_BLUE.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))
BOARD_BROWN_2 = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_BROWN-2.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))
BOARD_BROWN_3 = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_BROWN-3.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))
BOARD_PINK = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_PINK.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))
BOARD_RED = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_RED.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))
BOARD_COCO_MARTHEME = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_COCO_MARTHEME.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))
BOARD_SUISEI = pygame.transform.smoothscale(pygame.image.load('assets\\BOARD_SUISEI_2.png'), (BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET))

BOARD_W = BOARD_BLACK.get_width()
BOARD_H = BOARD_BLACK.get_height()

CROWN = pygame.transform.scale(pygame.image.load('assets\crown.png'), (25, 14))
