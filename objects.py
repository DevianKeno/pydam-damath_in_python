import pygame
from assets import *
from audio_constants import SOUND_VOLUME, MUSIC_VOLUME
from display_constants import *
from ui_class.colors import *
from ui_class.dropdown_menu import Dropdown
from ui_class.image import Image
from ui_class.new_btn import NButton, ButtonGroup
from ui_class.rect_window import RectWindow
from ui_class.textlist import TextList
from ui_class.tween import *
from ui_class.main_menu import Sidebar
from ui_class.window import Window
from ui_class.mode_window import ModeWindow
from ui_class.rect_window import create_window
from ui_class.fade_anim import Fade
from ui_class.slider import Slider

# --------- Fonts --------- 

font_cookie_run_reg = pygame.font.Font('font\CookieRun_Regular.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))
font_cookie_run_bold = pygame.font.Font('font\CookieRun_Bold.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))
font_cookie_run_blk = pygame.font.Font('font\CookieRun_Black.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))

# --------- Game Scene --------- 

game_side_surface = pygame.Surface((SCREEN_WIDTH*0.3, SCREEN_HEIGHT))
board_area_surface = pygame.Surface((SCREEN_WIDTH*0.7, SCREEN_HEIGHT))

# --------- MAIN MENU'S SIDE MENU OBJECTS ---------
menu_fontsize         = int(SIDE_MENU_RECT_ACTIVE.height*0.045)
mainmenu_opt_gap      = menu_fontsize * 2.1
side_menu_surface     = pygame.Surface((SCREEN_WIDTH*0.3, SCREEN_HEIGHT))
title_surface         = pygame.Surface((SCREEN_WIDTH*0.7, SCREEN_HEIGHT))

# --------- Main Menu --------- 

title = Image(TITLE, title_surface,
              (title_surface.get_width()//2, title_surface.get_height()//2),
              (TITLE.get_width(), TITLE.get_height()))

anim_title_slide_up = Move(title, (title.x, SCREEN_HEIGHT*0.1), 1, ease_type=easeInOutSine)
anim_title_slide_past_screen = Move(title, (title.x, 0-TITLE.get_height()), 1, ease_type=easeInOutSine, init_pos=(title.x, SCREEN_HEIGHT*0.1))
anim_title_slide_down = Move(title, (title.x, SCREEN_HEIGHT*0.1), 1, ease_type=easeInOutSine, init_pos=(title.x, 0-TITLE.get_height()))
anim_title_breathe = Move(title, (title.x, title.y+20), 1, ease_type=easeInOutSine, loop=ping_pong)
anim_title_squeeze = Scale(title, (1, 1.5), 1, ease_type=easeInOutSine, loop=ping_pong)
anim_title_rotate  = Rotate(title, 360, 1, ease_type=easeInOutElastic, loop=clamp)

# --------- fade screen object ---------
screen_copy = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
fade_screen = Fade(screen, screen_copy, pygame.Color(OAR_BLUE), (SIDE_MENU_RECT_CURRENT.width + (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/11, 0), speed=25)

# --------- Sliders --------- 
slider_color = (65, 87, 110)
music_slider = Slider(screen, slider_color, (int(SIDE_MENU_RECT_CURRENT.width + (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/2.5), int(SCREEN_HEIGHT/1.75)), int(SCREEN_WIDTH*0.3), 5, border_radius=8, circle_x=MUSIC_VOLUME)
sound_slider = Slider(screen, slider_color, (int(SIDE_MENU_RECT_CURRENT.width + (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/2.5), int(SCREEN_HEIGHT/1.50)), int(SCREEN_WIDTH*0.3), 5, border_radius=8, circle_x=SOUND_VOLUME)


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

right_captured_pieces_rect = pygame.Rect((board_area_surface.get_width() * 0.843, board_area_surface.get_height() * 0.075),
                                      (board_area_surface.get_width() * 0.148, board_area_surface.get_height() * 0.876))
right_captured_pieces_surface = pygame.Surface((right_captured_pieces_rect.w, right_captured_pieces_rect.h))

left_captured_pieces_rect = pygame.Rect((board_area_surface.get_width() * 0.0117, board_area_surface.get_height() * 0.075),
                                      (board_area_surface.get_width() * 0.148, board_area_surface.get_height() * 0.876))
left_captured_pieces_surface = pygame.Surface((left_captured_pieces_rect.w, left_captured_pieces_rect.h))

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

scoreboard_p1_chip_pos = scoreboard_p1_chip.pos

scoreboard_p2_chip = Image(ORANGE_PIECE, game_side_surface,
                           (scoreboard_p2_score_area.x+scoreboard_p2_score_area.w*0.1, scoreboard_p2_score_area.y+scoreboard_p2_score_area.h*0.15),
                           (game_side_surface.get_width()*0.213, game_side_surface.get_height()*0.13))

scoreboard_p2_chip_pos = scoreboard_p2_chip.pos

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

btn_size = (SCREEN_WIDTH*0.1607, SCREEN_HEIGHT*0.075)

classic_btn = NButton(screen, (SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10, 
                        SCREEN_HEIGHT/2), btn_size[0], btn_size[1], text='Classic', args='Classic',
                        tooltip_text="The classic game of Damath.", toggleable=True)
speed_btn = NButton(screen, (((SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10 + 
                        btn_size[0])+(SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width) - 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10 - 
                        btn_size[0]))/2 - btn_size[0]/2, SCREEN_HEIGHT/2),
                        btn_size[0], btn_size[1], text='Speed', args='Speed',
                        tooltip_text='Fast-paced game of Damath.', toggleable=True)
custom_btn = NButton(screen, ((SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width) - 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10 - 
                        btn_size[0]), SCREEN_HEIGHT/2), btn_size[0], 
                        btn_size[1], text='Custom',
                        tooltip_text='Create your own variation!', toggleable=True)
start_select_btn = NButton(screen, ((SIDE_MENU_RECT_CURRENT.width + 
                            SCREEN_WIDTH)/2 - btn_size[0]//2,
                            SCREEN_HEIGHT/1.25), btn_size[0],
                            btn_size[1], text='Start', rect_color=(38, 73, 89), 
                            hover_color=(30, 58, 71), selected_color=(30, 58, 71),
                            shadow_rect_color=(14, 33, 41), shadow_hovered_color=(16, 30, 37),
                            shadow_selected_color=(16, 30, 37), border_radius=10)

modes_btn = [classic_btn, speed_btn, custom_btn]
modes_btn_group = ButtonGroup(modes_btn, 1, True, caller_btn=start_select_btn, pass_target=False, pass_args=True)

# --------- Sidebar objects --------- 
sidebar = Sidebar(screen, (0, 0), SIDE_MENU_RECT_DEFAULT.w, SIDE_MENU_RECT_DEFAULT.h)

sidebar.add_option(3, "sb_play", pos=(SIDE_MENU_RECT_ACTIVE.width/4, 
                side_menu_surface.get_height()/2.5+mainmenu_opt_gap*0.15), text='Play', description='Play Damath!',
                icon=play_icon)
sidebar.add_option(3, "sb_online", pos=(SIDE_MENU_RECT_ACTIVE.width/4, 
                side_menu_surface.get_height()/2.5+(1*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                text='Multi', description='Play with friends!', 
                icon=online_icon)
sidebar.add_option(3, "sb_help", pos=(SIDE_MENU_RECT_ACTIVE.width/4, 
                side_menu_surface.get_height()/2.5+(2*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                text='Help', description='Learn Damath!', 
                icon=help_icon, icon_offset=55)
sidebar.add_option(3, "sb_options", pos=(SIDE_MENU_RECT_ACTIVE.width/4, 
                side_menu_surface.get_height()/2.5+(3*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                text='Options', description='Adjust to your preferences!', 
                icon=option_icon)
sidebar.add_option(3, "sb_exit", pos=(SIDE_MENU_RECT_ACTIVE.width/4, 
                side_menu_surface.get_height()/2.5+(4*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                    text='Exit', description='Quit the game... :<', 
                    icon=exit_icon)

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

icon_forfeit = Image(ICON_FORFEIT, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))
icon_offer_draw = Image(ICON_OFFER_DRAW, screen, (0, 0), (screen.get_width()*0.0166, screen.get_height()*0.03))

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

__pause_btn_pos = (((SCREEN_WIDTH*0.5-pause_window.width*0.5)+
                (pause_window.w*0.5-(pause_window.w*0.45)*0.5)),
                SCREEN_HEIGHT*0.5-pause_window.h*0.5+
                pause_window.h*0.25)
__pause_btn_size = (pause_window.w*0.465, btn_size[1])              
__pause_btn_kwargs = {
                "rect_color" : TEAL,
                "shadow_rect_color" : DARKER_TEAL,
                "shadow_offset" : (pause_window.w*0.45)*0.05,
                "fontsize" : int((pause_window.h*0.175) * 0.4)
                }

resume_btn = NButton(screen, __pause_btn_pos, *__pause_btn_size, 
                text='Resume', **__pause_btn_kwargs)
options_btn = NButton(screen, (__pause_btn_pos[0], __pause_btn_pos[1]+btn_size[1]*1.35), 
                *__pause_btn_size,  text='Options', **__pause_btn_kwargs)
restart_btn = NButton(screen, (__pause_btn_pos[0], __pause_btn_pos[1]+btn_size[1]*2.7), 
                *__pause_btn_size, text='Restart', **__pause_btn_kwargs)
main_menu_btn = NButton(screen, (__pause_btn_pos[0], __pause_btn_pos[1]+btn_size[1]*4), 
                *__pause_btn_size, text='Main Menu', **__pause_btn_kwargs)

pause_buttons = [resume_btn, options_btn, restart_btn, main_menu_btn]
pause_buttons_group = ButtonGroup(pause_buttons)

# --------- Toggleables Window Objects  --------- 

# ----- symbols  -----
add_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='+', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            fontstyle='font/CookieRun_Bold.ttf', toggleable=True)
sub_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='-', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            fontstyle='font/CookieRun_Bold.ttf', toggleable=True)
mul_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='×', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            fontstyle='font/CookieRun_Bold.ttf', toggleable=True)
div_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='÷', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            fontstyle='font/CookieRun_Bold.ttf', toggleable=True)
random_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='?', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            fontstyle='font/CookieRun_Bold.ttf', toggleable=True)

symbols_btn = {
    add_btn: False,
    sub_btn: False,
    mul_btn: False,
    div_btn: False,
    random_btn: False
}

for key in [symbol for symbol in symbols_btn.keys()][:4]:
    key.set_state(NButton.Toggled)

# ----- values  -----
none_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='None', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.0275),
            fontstyle='font/CookieRun_Bold.ttf')
naturals_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='1', shadow_offset=8,
            fontstyle='font/CookieRun_Bold.ttf')
integers_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='-2', shadow_offset=8,
            fontstyle='font/CookieRun_Bold.ttf')
rationals_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='⅓', shadow_offset=8,
            fontstyle='font/CookieRun_Bold.ttf')
radicals_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='√', shadow_offset=8,
            fontstyle='font/CookieRun_Bold.ttf')
polynomial_btn = NButton(screen, (0, 0), int(SIDE_MENU_RECT_ACTIVE.height*0.08),
            int(SIDE_MENU_RECT_ACTIVE.height*0.08), text='XY', shadow_offset=8,
            border_radius=16, fontsize=int(SIDE_MENU_RECT_ACTIVE.height*0.04),
            fontstyle='font/CookieRun_Bold.ttf')

# --------- Multi Menu Button Objects  --------- 
multi_local_btn = NButton(screen, (((SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10 + 
                        btn_size[0])+(SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width) - 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10 - 
                        btn_size[0]))/2 - btn_size[0]/2, SCREEN_HEIGHT/2),
                        btn_size[0], btn_size[1], text='Local', args='Local',
                        tooltip_text='Play with your friends!', toggleable=True)
multi_online_btn = NButton(screen, ((SIDE_MENU_RECT_CURRENT.width + 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width) - 
                        (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/10 - 
                        btn_size[0]), SCREEN_HEIGHT/2), btn_size[0], 
                        btn_size[1], text='Online',
                        tooltip_text='Not available yet.', toggleable=True)

multi_join_btn = NButton(screen, ((SIDE_MENU_RECT_CURRENT.width + 
                            SCREEN_WIDTH)/2 - btn_size[0]//2,
                            SCREEN_HEIGHT/1.25), btn_size[0],
                            btn_size[1], text='Join', rect_color=(38, 73, 89), 
                            hover_color=(30, 58, 71), selected_color=(30, 58, 71),
                            shadow_rect_color=(14, 33, 41), shadow_hovered_color=(16, 30, 37),
                            shadow_selected_color=(16, 30, 37), border_radius=10)

multi_button_group = ButtonGroup([multi_local_btn, multi_online_btn], 1, True)