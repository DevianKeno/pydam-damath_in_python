"""
Assets initialization.
"""

import pygame
from damath.constants import *

# --------- x --------- 

BOARD = pygame.image.load('new_assets\\board_default.png').convert_alpha()
BOARD_SHADOW = pygame.image.load('new_assets\\board_shadow_bg.png').convert()

BLUE_PIECE = pygame.image.load('new_assets\chips\chip_blue.png').convert_alpha()
ORANGE_PIECE = pygame.image.load('new_assets\chips\chip_orange.png').convert_alpha()
RED_PIECE = pygame.image.load('assets\piece_red.png').convert_alpha()

BLUE_PIECE_KING = pygame.image.load('new_assets\chips\chip_blue_king.png').convert_alpha()
ORANGE_PIECE_KING = pygame.image.load('new_assets\chips\chip_orange_king.png').convert_alpha()
RED_PIECE_KING = pygame.image.load('assets\piece_red_king.png').convert_alpha()

# --------- x --------- 

SCOREBOARD_SCORE_AREA = pygame.image.load('new_assets\scoreboard\score_area.png').convert_alpha()

SCOREBOARD_RED = pygame.transform.smoothscale(pygame.image.load('assets\SCOREBOARD_RED.png'), (250, 250))
SCOREBOARD_BLUE = pygame.transform.smoothscale(pygame.image.load('assets\SCOREBOARD_BLUE.png'), (250, 250))
SCOREBOARD_RED_ACTIVE = pygame.transform.smoothscale(pygame.image.load('assets\SCOREBOARD_RED_ACTIVE.png'), (250, 250))
SCOREBOARD_BLUE_ACTIVE = pygame.transform.smoothscale(pygame.image.load('assets\SCOREBOARD_BLUE_ACTIVE.png'), (250, 250))

# --------- Cheats GUI --------- 

CHEAT_WINDOW_BLUE = pygame.image.load('new_assets\cheats_window_blue.png').convert_alpha()
CHEAT_WINDOW_ORANGE = pygame.image.load('new_assets\cheats_window_orange.png').convert_alpha()

# Icons
ICON_ADD = pygame.image.load('new_assets\icons\icon_add_piece.png').convert_alpha()
ICON_REMOVE = pygame.image.load('new_assets\icons\icon_remove.png').convert_alpha()
ICON_PROMOTE = pygame.image.load('new_assets\icons\icon_promote.png').convert_alpha()
ICON_DEMOTE = pygame.image.load('new_assets\icons\icon_demote.png').convert_alpha()

# --------- x --------- 

# BOARD_1 = pygame.transform.smoothscale(pygame.image.load('assets\\vecteezy_chess-board-cropped.jpg'), (BOARD_WIDTH-5, BOARD_HEIGHT-5))
BOARD_BLACK = pygame.transform.smoothscale(pygame.image.load('new_assets\\board_default_copy.png'), (BOARD_THEME_W, BOARD_THEME_H)).convert_alpha()
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