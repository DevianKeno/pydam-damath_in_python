

import pygame
from display_constants import *
from assets import BOARD
from ui_class.title import Image

# --------- Game Scene --------- 

game_side_surface = pygame.Surface((SCREEN_WIDTH*0.3, SCREEN_HEIGHT))
board_area_surface = pygame.Surface((SCREEN_WIDTH*0.7, SCREEN_HEIGHT))

damath_board = Image(BOARD, board_area_surface,
              (board_area_surface.get_width()//2, board_area_surface.get_height()//2),
              (board_area_surface.get_width()*0.744, board_area_surface.get_height()*0.926))

tiles_rect = pygame.Rect((0, 0), (damath_board.w*0.765, damath_board.h*0.765))
tiles_rect.center = (board_area_surface.get_width()//2, board_area_surface.get_height()//2)

chips_surface = pygame.Surface((tiles_rect.w, tiles_rect.h))

SQUARE_SIZE = chips_surface.get_width()//8