import pygame
from assets import *
from display_constants import *
from ui_class.colors import *
from ui_class.dropdown_menu import Dropdown
from ui_class.image import Image
from ui_class.new_btn import NButton
from ui_class.rect_window import RectWindow
from ui_class.textlist import TextList
from ui_class.tween import *
from ui_class.main_menu import Sidebar
from ui_class.window import Window
from ui_class.mode_window import ModeWindow
from ui_class.rect_window import create_window

# --------- Fonts --------- 

font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))
font_cookie_run_bold = pygame.font.Font('font\CookieRun_Bold.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))
font_cookie_run_blk = pygame.font.Font('font\CookieRun_Black.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))

# --------- Game Scene --------- 

game_side_surface = pygame.Surface((SCREEN_WIDTH*0.3, SCREEN_HEIGHT))
board_area_surface = pygame.Surface((SCREEN_WIDTH*0.7, SCREEN_HEIGHT))


# --------- Damath Board --------- 

damath_board = Image(BOARD, board_area_surface,
                     (board_area_surface.get_width()//2, board_area_surface.get_height()//2),
                     (board_area_surface.get_width()*0.744, board_area_surface.get_height()*0.926))

damath_board_shadow = Image(BOARD_SHADOW, board_area_surface,
                     (board_area_surface.get_width()//2-1, board_area_surface.get_height()//2),
                     (board_area_surface.get_width(), board_area_surface.get_height()))

# --------- Damath Board Coordinates --------- 

board_x_coords_rect = pygame.Rect((damath_board.x+damath_board.w*0.08, damath_board.y+damath_board.h*0.924),
                                  (damath_board.w*0.84, damath_board.h*0.034))
board_y_coords_rect = pygame.Rect((damath_board.x+damath_board.w*0.045, damath_board.y+damath_board.h*0.08),
                                  (damath_board.w*0.034, damath_board.h*0.84))

board_x_coords_surface = pygame.Surface((board_x_coords_rect.w, board_x_coords_rect.h))
board_y_coords_surface = pygame.Surface((board_y_coords_rect.w, board_y_coords_rect.h))

tiles_rect = pygame.Rect((0, 0), (damath_board.w*0.833, damath_board.h*0.833))
tiles_rect.center = (board_area_surface.get_width()//2, board_area_surface.get_height()//2)

chips_surface = pygame.Surface((tiles_rect.w, tiles_rect.h))

p1_captured_pieces_rect = pygame.Rect((board_area_surface.get_width() * 0.843, board_area_surface.get_height() * 0.075),
                                      (board_area_surface.get_width() * 0.148, board_area_surface.get_height() * 0.876))
p1_captured_pieces_surface = pygame.Surface((p1_captured_pieces_rect.w, p1_captured_pieces_rect.h))

p2_captured_pieces_rect = pygame.Rect((board_area_surface.get_width() * 0.0117, board_area_surface.get_height() * 0.075),
                                      (board_area_surface.get_width() * 0.148, board_area_surface.get_height() * 0.876))
p2_captured_pieces_surface = pygame.Surface((p2_captured_pieces_rect.w, p2_captured_pieces_rect.h))

selection_guide_rect = pygame.Rect((0, 0), (SCREEN_WIDTH*0.433, SCREEN_HEIGHT*0.111))

square_size = chips_surface.get_width()//8

mini_title = Image(TITLE, game_side_surface,
                   (game_side_surface.get_width()//2, game_side_surface.get_height()*0.1),
                   (game_side_surface.get_width()*0.585, game_side_surface.get_height()*0.069))

text_scores = font_cookie_run_bold.render("Scores", True, OAR_BLUE)

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

cheats_window_blue = Window(CHEAT_WINDOW_BLUE, screen,
                            (0, 0),
                            (screen.get_width()*0.097, screen.get_height()*0.096))
cheats_window_orange = Window(CHEAT_WINDOW_ORANGE, screen,
                              (0, 0),
                              (screen.get_width()*0.097, screen.get_height()*0.096))
                              
cheats_window_blue_long = Window(CHEAT_WINDOW_BLUE_LONG, screen,
                            (0, 0),
                            (screen.get_width()*0.12, screen.get_height()*0.096))
cheats_window_orange_long = Window(CHEAT_WINDOW_ORANGE_LONG, screen,
                              (0, 0),
                              (screen.get_width()*0.12, screen.get_height()*0.096))

# --------- Buttons  --------- 

btn_size = (SCREEN_WIDTH*0.1607, SCREEN_HEIGHT*0.06)
classic_btn = NButton(screen, (SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10, 
                        SCREEN_HEIGHT/2), btn_size[0], btn_size[1], 'Classic', args='Classic')
speed_btn = NButton(screen, (((SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10 + 
                        btn_size[0])+(SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width) - 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10 - 
                        btn_size[0]))/2 - btn_size[0]/2, SCREEN_HEIGHT/2),
                        btn_size[0], btn_size[1], 'Speed', args='Speed')
custom_btn = NButton(screen, ((SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width) - 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10 - 
                        btn_size[0]), SCREEN_HEIGHT/2), btn_size[0], 
                        btn_size[1], 'Custom', args='Custom')
start_select_btn = NButton(screen, ((SIDE_MENU_RECT_CURRENT.width + 
                            SCREEN_WIDTH)/2 - btn_size[0]//2,
                            SCREEN_HEIGHT/1.25), btn_size[0],
                            btn_size[1], 'Start', rect_color=(38, 73, 89), 
                            hover_color=(30, 58, 71), selected_color=(30, 58, 71),
                            shadow_rect_color=(14, 33, 41), shadow_hovered_color=(16, 30, 37),
                            shadow_selected_color=(16, 30, 37), border_radius=10)

toggle_btn = {
    classic_btn : False,
    speed_btn : False,
    custom_btn : False
}

# --------- Sidebar objects --------- 
sidebar = Sidebar(screen, (0, 0), SIDE_MENU_RECT_DEFAULT.w, SIDE_MENU_RECT_DEFAULT.h)

# --------- Mode Toggleables Window  --------- 

mode_window = ModeWindow(screen, (sidebar.sidebar_rect.x+
                (0.0075*sidebar.sidebar_rect.w), SCREEN_HEIGHT*0.5),
                200, 300, '#486582', border_color='#425D78', 
                border_radius=10, border_thickness=8, button_pos=(0, 0),
                button_width=125, button_height=50, button_text=" ",
                button_shadow_offset=8)

# --------- Text Lists  --------- 

icon_add = Image(ICON_ADD, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))
icon_remove = Image(ICON_REMOVE, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))
icon_promote = Image(ICON_PROMOTE, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))
icon_demote = Image(ICON_DEMOTE, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))

icon_change_turn = Image(ICON_CHANGE_TURN, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))
icon_remove_all = Image(ICON_REMOVE_ALL, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))
icon_promote_all = Image(ICON_PROMOTE_ALL, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))
icon_demote_all = Image(ICON_DEMOTE_ALL, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))
icon_pause_timer = Image(ICON_PAUSE_TIMER, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))
icon_resume_timer = Image(ICON_RESUME_TIMER, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))

# --------- Pause Window Objects  --------- 

alpha_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
alpha_surface.fill(DARK_GRAY_BLUE)
alpha_surface.set_alpha(125)

pause_font = pygame.font.Font('font/CookieRun_Regular.ttf', int((SCREEN_HEIGHT*0.575)*0.1))
pause_text = pause_font.render('Paused', True, WHITE)

pause_window = create_window(screen, (0, 0), 
                SCREEN_WIDTH*0.285, SCREEN_HEIGHT*0.575,
                DARK_BLUE, border_radius=10,
                cast_shadow=False)

resume_btn = NButton(screen, ((SCREEN_WIDTH*0.5-pause_window.width*0.5)+
                (pause_window.w*0.5-(pause_window.w*0.45)*0.5), 
                (SCREEN_HEIGHT*0.5-pause_window.h*0.5)+
                (pause_window.h*0.25)), pause_window.w*0.45, 
                btn_size[1], 'Resume', rect_color=TEAL, shadow_rect_color=DARKER_TEAL,
                shadow_offset=(pause_window.w*0.45)*0.05)

options_btn = NButton(screen, ((SCREEN_WIDTH*0.5-pause_window.width*0.5)+
                (pause_window.w*0.5-(pause_window.w*0.45)*0.5), 
                (SCREEN_HEIGHT*0.5-pause_window.h*0.5)+
                (pause_window.h*0.25+btn_size[1]*1.75)), pause_window.w*0.45, 
                btn_size[1], 'Options', rect_color=TEAL, shadow_rect_color=DARKER_TEAL,
                shadow_offset=(pause_window.w*0.45)*0.05)

restart_btn = NButton(screen, ((SCREEN_WIDTH*0.5-pause_window.width*0.5)+
                (pause_window.w*0.5-(pause_window.w*0.45)*0.5), 
                (SCREEN_HEIGHT*0.5-pause_window.h*0.5)+
                (pause_window.h*0.25+btn_size[1]*3.5)), pause_window.w*0.45, 
                btn_size[1], 'Restart', rect_color=TEAL, shadow_rect_color=DARKER_TEAL,
                shadow_offset=(pause_window.w*0.45)*0.05)

main_menu_btn = NButton(screen, ((SCREEN_WIDTH*0.5-pause_window.width*0.5)+
                (pause_window.w*0.5-(pause_window.w*0.45)*0.5), 
                (SCREEN_HEIGHT*0.5-pause_window.h*0.5)+
                (pause_window.h*0.25+btn_size[1]*5.25)), pause_window.w*0.45, 
                btn_size[1], 'Main Menu', rect_color=TEAL, shadow_rect_color=DARKER_TEAL,
                shadow_offset=(pause_window.w*0.45)*0.05)

pause_btns = {
    resume_btn : False,
    options_btn : False,
    restart_btn : False,
    main_menu_btn : False    
}

# --------- Toggleables Window Objects  --------- 

# ----- symbols  -----
add_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), '+', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            fontstyle='font/CookieRun_Bold.ttf')
sub_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), '-', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            fontstyle='font/CookieRun_Bold.ttf')
mul_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), '×', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            fontstyle='font/CookieRun_Bold.ttf')
div_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), '÷', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            fontstyle='font/CookieRun_Bold.ttf')
random_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), '?', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            fontstyle='font/CookieRun_Bold.ttf')

symbols_btn = {
    add_btn: False,
    sub_btn: False,
    mul_btn: False,
    div_btn: False,
    random_btn: False
}

for key in [symbol for symbol in symbols_btn.keys()][:4]:
    key.toggled = True
    key.set_state(NButton.Toggled)

# ----- values  -----
none_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), 'None', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.0275),
            fontstyle='font/CookieRun_Bold.ttf')
naturals_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), '1', shadow_offset=8,
            fontstyle='font/CookieRun_Bold.ttf')
integers_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), '-2', shadow_offset=8,
            fontstyle='font/CookieRun_Bold.ttf')
rationals_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), '⅓', shadow_offset=8,
            fontstyle='font/CookieRun_Bold.ttf')
radicals_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), '√', shadow_offset=8,
            fontstyle='font/CookieRun_Bold.ttf')
polynomial_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), 'XY', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.04),
            fontstyle='font/CookieRun_Bold.ttf')
