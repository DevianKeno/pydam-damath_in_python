import pygame
from assets import BOARD, BOARD_SHADOW, SCOREBOARD_SCORE_AREA, BLUE_PIECE, ORANGE_PIECE
from display_constants import *
from ui_class.colors import *
from ui_class.image import Image
from ui_class.tween import *


# --------- Fonts --------- 

font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))
font_cookie_run_bold = pygame.font.Font('font\CookieRun_Bold.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))
font_cookie_run_blk = pygame.font.Font('font\CookieRun_Black.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))

# --------- Game Scene --------- 

game_side_surface = pygame.Surface((SCREEN_WIDTH*0.3, SCREEN_HEIGHT))
board_area_surface = pygame.Surface((SCREEN_WIDTH*0.7, SCREEN_HEIGHT))

damath_board = Image(BOARD, board_area_surface,
                     (board_area_surface.get_width()//2, board_area_surface.get_height()//2),
                     (board_area_surface.get_width()*0.744, board_area_surface.get_height()*0.926))

damath_board_shadow = Image(BOARD_SHADOW, board_area_surface,
                     (board_area_surface.get_width()//2-1, board_area_surface.get_height()//2),
                     (board_area_surface.get_width(), board_area_surface.get_height()))


tiles_rect = pygame.Rect((0, 0), (damath_board.w*0.833, damath_board.h*0.833))
tiles_rect.center = (board_area_surface.get_width()//2, board_area_surface.get_height()//2)

chips_surface = pygame.Surface((tiles_rect.w, tiles_rect.h+tiles_rect.h))

p1_captured_pieces_rect = pygame.Rect((board_area_surface.get_width() * 0.843, board_area_surface.get_height() * 0.075), (150, board_area_surface.get_height() * 0.876))
p1_captured_pieces_surface = pygame.Surface((p1_captured_pieces_rect.w, p1_captured_pieces_rect.h))

p2_captured_pieces_rect = pygame.Rect((board_area_surface.get_width() * 0.0035, board_area_surface.get_height() * 0.075), (150, board_area_surface.get_height() * 0.876))
p2_captured_pieces_surface = pygame.Surface((p2_captured_pieces_rect.w, p2_captured_pieces_rect.h))

selection_guide_rect = pygame.Rect((0, 0), (SCREEN_WIDTH*0.433, SCREEN_HEIGHT*0.111))

square_size = chips_surface.get_width()//8

mini_title = Image(TITLE, game_side_surface,
                   (game_side_surface.get_width()//2, game_side_surface.get_height()*0.1),
                   (game_side_surface.get_width()*0.585, game_side_surface.get_height()*0.069))

text_scores = font_cookie_run_bold.render("Scores", True, OAR_BLUE)
text_mode = font_cookie_run_reg.render("Classic", True, OAR_BLUE)

scoreboard_surface  = pygame.Surface((game_side_surface.get_width(), game_side_surface.get_height()))
scoreboard_rect = scoreboard_surface.get_rect()

scoreboard_p1_score_area = Image(SCOREBOARD_SCORE_AREA, game_side_surface,
                              (game_side_surface.get_width()//2, game_side_surface.get_height()*0.45),
                              (game_side_surface.get_width()*0.722, game_side_surface.get_height()*0.226))

scoreboard_p2_score_area = Image(SCOREBOARD_SCORE_AREA, game_side_surface,
                              (game_side_surface.get_width()//2, game_side_surface.get_height()*0.70),
                              (game_side_surface.get_width()*0.722, game_side_surface.get_height()*0.226))

scoreboard_p1_chip = Image(BLUE_PIECE, game_side_surface,
                           (scoreboard_p1_score_area.x+scoreboard_p1_score_area.w*0.1, scoreboard_p1_score_area.y+scoreboard_p1_score_area.h*0.15),
                           (game_side_surface.get_width()*0.213, game_side_surface.get_height()*0.13))

scoreboard_p2_chip = Image(ORANGE_PIECE, game_side_surface,
                           (scoreboard_p2_score_area.x+scoreboard_p2_score_area.w*0.1, scoreboard_p2_score_area.y+scoreboard_p2_score_area.h*0.15),
                           (game_side_surface.get_width()*0.213, game_side_surface.get_height()*0.13))

# scoreboard_rect     = pygame.Rect(SIDE_MENU_RECT_ACTIVE.w//2-SCOREBOARD_WIDTH//2, SIDE_MENU_RECT_ACTIVE.h//1.8-SCOREBOARD_HEIGHT//2, SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)
