# 
# Damath
# 

import pygame 
import sys
import random 
import threading
from math import ceil
from damath.board import Board
from damath.cheats import Cheats
from damath.game import Game
from damath.piece import Piece
from damath.scoreboard import Scoreboard
from damath.constants import *
from damath.timer import *
from display_constants import *
from ui_class.button import Button, ButtonList
from ui_class.new_btn import NButton
from ui_class.colors import *
from ui_class.constants import START_BTN_DIMENSION, START_BTN_POSITION
from ui_class.fade import *
from ui_class.fade_anim import Fade
from ui_class.main_menu import *
from ui_class.themes_option import Themes, ThemesList
from ui_class.image import *
from ui_class.tween import *
from ui_class.slider import Slider
from ui_class.rect_window import *
from audio_constants import * 
from objects import *
from assets import *
from options import *

# --------- initialization ---------
pygame.init()
pygame.font.init()
pygame.mixer.init(44100, -16, 2, 2048)

# --------- defining constants / objects for screen  ---------

ANIM_SPEED  = 20
ANIM_ALPHA  = 255
CHIP_WIDTH  = 360
CHIP_HEIGHT = 240

clock = pygame.time.Clock()
font  = pygame.font.Font('font\CookieRun_Bold.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))    

# --------- piece move function ---------
def get_row_col_from_mouse(pos):
    x, y = pos
    row = (y-selection_guide_rect.h) // square_size
    col = (x-selection_guide_rect.w) // square_size
    return row, col

def anim_dim():
    return random.randrange(0-CHIP_WIDTH, SCREEN_WIDTH, 1), 0-CHIP_HEIGHT

def show_score():
    score = round(max(game.scoreboard.score()), 2)
    font = pygame.font.Font('font\CookieRun_Bold.ttf', 100).render(str(score), True, WHITE)
    #score_rect = pygame.Rect(255, 165, 535, 235)
    screen.blit(font, (SCREEN_WIDTH//2 - font.get_width()//2 - 12, SCREEN_HEIGHT//(2.8)))

SOUNDS = [POP_SOUND, MOVE_SOUND, 
          SWEEP_SOUND, SELECT_SOUND, 
          CAPTURE_SOUND, INVALID_SOUND,
          TRANSITION_IN_SOUND, 
          TRANSITION_OUT_SOUND]

def change_volume(vol):
    for sound in SOUNDS:
        sound.set_volume(vol)

change_volume(SOUND_VOLUME)

# --------- Falling Spinning Chip Animation assets ---------
chip_animation = False

if chip_animation:
    class FallingSpinningChip:

        def __init__(self, screen, color):
            self.screen = screen
            self.color = color
            self._init()
            self.frame = 0
            self.delay = 0
            self.delayed = False

        def _init(self):
            self.width, self.height = anim_dim()

        def next_frame(self):
            if self.height == -180 and not self.delayed:
                self.delay = random.randint(1, 300)
                self.height = self.height - self.delay
                self.delayed = True
            
            if self.height > SCREEN_HEIGHT:
                self.reset()

            if self.delay:
                self.height += 1
                self.delay -= 1
            else:
                self.height += ANIM_SPEED

                if self.frame == len(frames_blue)-1:
                    self.frame =  0
                else:
                    self.frame += 1

                if self.color == 'blue':
                    frames_blue[self.frame].set_alpha(ANIM_ALPHA)
                    self.screen.blit(frames_blue[self.frame], (self.width, self.height))
                else:
                    frames_red[self.frame].set_alpha(ANIM_ALPHA)
                    self.screen.blit(frames_red[self.frame], (self.width, self.height))
        
        def reset(self):
            self._init()

    # --------- In-Place Spinning Chip Animation assets ---------

    class SpinningChip:
        
        def __init__(self, screen, color):
            self.screen = screen
            self.color = color
            self.frame = 0

        def play(self):

            if self.frame == len(frames_blue_big)-1:
                self.frame = 0
            else:
                self.frame += 1

            if self.color == 'red':
                frames_red_big[self.frame].set_alpha(ANIM_ALPHA)
                self.screen.blit(frames_red_big[self.frame], (SCREEN_WIDTH//3-(frames_red_big[self.frame].get_width()//2), SCREEN_HEIGHT//2-(frames_red_big[self.frame].get_height()//2)))
            else:
                frames_blue_big[self.frame].set_alpha(ANIM_ALPHA)
                self.screen.blit(frames_blue_big[self.frame], (SCREEN_WIDTH//3.-(frames_red_big[self.frame].get_width()//2), SCREEN_HEIGHT//2-(frames_red_big[self.frame].get_height()//2)))           

    # --------- loading chip frames ---------

    blue_chips = []
    red_chips  = []

    for i in range(8):
        if (i%2 == 0):
            blue_chips.append(FallingSpinningChip(screen, 'blue'))
        else:
            red_chips.append(FallingSpinningChip(screen, 'red'))

    # --------- animation assets ---------
    frames_blue = []
    for i in range(1, 462):
        if i < 10:
            frame = pygame.transform.smoothscale(pygame.image.load(f'assets/anim_lowres/blue/000{i}.png'), (CHIP_WIDTH, CHIP_HEIGHT))
        elif i < 100:
            frame = pygame.transform.smoothscale(pygame.image.load(f'assets/anim_lowres/blue/00{i}.png'), (CHIP_WIDTH, CHIP_HEIGHT))  
        else:
            frame = pygame.transform.smoothscale(pygame.image.load(f'assets/anim_lowres/blue/0{i}.png'), (CHIP_WIDTH, CHIP_HEIGHT))  

        frames_blue.append(frame)

    frames_red = []

    for i in range(1, 462):
        if i < 10:
            frame = pygame.transform.smoothscale(pygame.image.load(f'assets/anim_lowres/red/000{i}.png'), (CHIP_WIDTH, CHIP_HEIGHT))
        elif i < 100:
            frame = pygame.transform.smoothscale(pygame.image.load(f'assets/anim_lowres/red/00{i}.png'), (CHIP_WIDTH, CHIP_HEIGHT))  
        else:
            frame = pygame.transform.smoothscale(pygame.image.load(f'assets/anim_lowres/red/0{i}.png'), (CHIP_WIDTH, CHIP_HEIGHT))  

        frames_red.append(frame)

    frames_blue_big = []

    for i in range(1, 462):
        if i < 10:
            frame = pygame.image.load(f'assets/anim_lowres/blue/000{i}.png')
        elif i < 100:
            frame = pygame.image.load(f'assets/anim_lowres/blue/00{i}.png') 
        else:
            frame = pygame.image.load(f'assets/anim_lowres/blue/0{i}.png')

        frames_blue_big.append(frame)   

    frames_red_big = []

    for i in range(1, 462):
        if i < 10:
            frame = pygame.image.load(f'assets/anim_lowres/red/000{i}.png')
        elif i < 100:
            frame = pygame.image.load(f'assets/anim_lowres/red/00{i}.png') 
        else:
            frame = pygame.image.load(f'assets/anim_lowres/red/0{i}.png')

        frames_red_big.append(frame)   

# --------- MAIN MENU'S SIDE MENU OBJECTS ---------
menu_fontsize         = int(SIDE_MENU_RECT_ACTIVE.height*0.045)
mainmenu_opt_gap      = menu_fontsize * 2.1
side_menu_surface     = pygame.Surface((SCREEN_WIDTH*0.3, SCREEN_HEIGHT))
title_surface         = pygame.Surface((SCREEN_WIDTH*0.7, SCREEN_HEIGHT))

# --------- instantiating Start button ---------
start_btn = Button(screen, START_BTN_DIMENSION[0], START_BTN_DIMENSION[1], START_BTN_POSITION, 4, None, text='Start', fontsize=36) # w, h, (x, y), radius, image=None, text

# --------- instantiating Options button ---------
option_img_filepath = 'img\\settings-25-512.png'
option_img          = pygame.transform.smoothscale(pygame.image.load(option_img_filepath), (36, 36)).convert_alpha()
option_btn          = Button(screen, 80, 65, (SCREEN_WIDTH/2+150, (SCREEN_HEIGHT/4)*3), 4, image=option_img, image_size=(36, 36)) # w, h, (x, y), radius, image, text=None

# --------- instantiating the Return button ---------
return_img_filepath = 'img\\button-return.png'
RETURN_DIMENSION    = (30, 30)
return_img          = pygame.transform.smoothscale(pygame.image.load(return_img_filepath), (RETURN_DIMENSION)).convert_alpha()
return_btn          = Button(screen, 70, 70, (20, 20), 4, image=return_img, image_size=RETURN_DIMENSION) # w, h, (x, y), radius, image, text=None

# --------- list of available themes in the game ---------
themes = ThemesList(screen)

BOARDS = [BOARD_BLACK,   BOARD_GREEN, 
          BOARD_BROWN,   BOARD_LIGHTBROWN,
          BOARD_PINK,    BOARD_BROWN_2, 
          BOARD_BROWN_3, BOARD_BLUE, 
          BOARD_RED,     BOARD_COCO_MARTHEME]

for idx, board in enumerate(BOARDS):
    themes.append(Themes(screen, board, idx))

BOARD_DEFAULT_THEME = themes.list[themes.focused].board #black board

# --------- instantiating the Damath Board and Scoreboard  ---------

board_theme_surface = pygame.Surface((BOARD_THEME_W, BOARD_THEME_H))
board_theme_rect    = pygame.Rect(SCREEN_WIDTH*0.7//2+(SCREEN_WIDTH*0.3)-board_theme_surface.get_width()//2,
                                  SCREEN_HEIGHT//2-board_theme_surface.get_height()//2+10,
                                  BOARD_WIDTH, BOARD_HEIGHT)

board_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT)) # creating a Surface object where the board will be placed
board_rect    = pygame.Rect(SCREEN_WIDTH*0.7//2+(SCREEN_WIDTH*0.3)-board_surface.get_width()//2,
                            SCREEN_HEIGHT//2-board_surface.get_height()//2,
                            BOARD_WIDTH, BOARD_HEIGHT) #creating a Rect object to save the position & size of the board

board = Board(chips_surface, BOARD_DEFAULT_THEME)
scoreboard = Scoreboard(game_side_surface)
game = Game(chips_surface, board, scoreboard, BOARD_DEFAULT_THEME)

if CHEATS:
    cheats = Cheats(screen, game)

if chip_animation:  
    big_blue_chip = SpinningChip(screen, 'blue')
    big_red_chip  = SpinningChip(screen, 'red')

# --------- instantiating Pause objects ---------
paused_rect     = pygame.Rect((SCREEN_WIDTH//2, SCREEN_HEIGHT//2-200, 350, 400))
paused_surface  = pygame.Surface((paused_rect.w, paused_rect.h), pygame.SRCALPHA)
#paused_surface.set_colorkey((0, 0, 0))

# pause menu options
pause_return_btn = Button(screen, 70, 70, (20, 20), 4, image=return_img, image_size=RETURN_DIMENSION) # w, h, (x, y), radius, image, text=None

resume_btn        = Button(screen, 250, 50, (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//1.5-265), 5, None, text='Resume', fontsize=24)
restart_btn       = Button(screen, 250, 50, (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//1.5-190), 5, None, text='Restart', fontsize=24)
pause_options_btn = Button(screen, 250, 50, (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//1.5-115), 5, None, text='Options', fontsize=24)
quit_btn          = Button(screen, 250, 50, (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//1.5-40), 5, None, text='Quit Game', fontsize=24)

# --------- transition objects ---------
# --------- instantiating Transition objects ---------
transition_in_list = []

for i in range(51):
    if i < 10:
        frame =  pygame.transform.smoothscale(pygame.image.load(f'assets/anim_transition_in/000{i}.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        frame = pygame.transform.smoothscale(pygame.image.load(f'assets/anim_transition_in/00{i}.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))

    transition_in_list.append(frame)


transition_out_list = []

for i in range(37):

    frame =  pygame.transform.smoothscale(pygame.image.load(f'assets/anim_transition_out/00{i+50}.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    transition_out_list.append(frame)

# --------- Transition class ---------
class Transition:
    def __init__(self, screen, transition_list):
        self.screen = screen
        self.transition = transition_list
        self.frame = 0
        self.finished = False
        self.sound_played = False
    
    def play(self):
        
        if not self.sound_played:
            if self.transition == transition_in_list:
                TRANSITION_IN_SOUND.play()
                self.sound_played = True
            else:
                TRANSITION_OUT_SOUND.play()
                self.sound_played = True

        if self.frame == len(self.transition)-1:
            self.finished = True
        else:
            self.frame += 1
 
        self.screen.blit(self.transition[self.frame], (0, 0))

    def reset(self):
        self.frame = 0
        self.finished = False
        self.sound_played = False
    
    def get_finished(self):
        return self.finished

transition_in  = Transition(screen, transition_in_list)
transition_out = Transition(screen, transition_out_list)

def full_trans_play():

    if not transition_in.get_finished():
        transition_in.play()
    else:
        transition_out.play()

def full_trans_reset():

    transition_in.reset()
    transition_out.reset()

# --------- Main Menu --------- 

title = Image(TITLE, title_surface,
              (title_surface.get_width()//2, title_surface.get_height()//2),
              (title_surface.get_width()*0.942, title_surface.get_height()*0.261))

anim_title_up = Move(title, (title.x, SCREEN_HEIGHT//10), 1, ease_type=easeInOutSine)
anim_title_breathe = Move(title, (title.x, title.y+20), 1, ease_type=easeInOutSine, loop=ping_pong)
anim_title_squeeze = Scale(title, (1, 1.5), 1, ease_type=easeInOutSine, loop=ping_pong)
anim_title_rotate  = Rotate(title, 360, 1, ease_type=easeInOutElastic, loop=clamp)

# --------- Side menu rect tweenable --------- 
TEST_side_menu = pygame.Rect(0, 0, SCREEN_WIDTH*0.15, SCREEN_HEIGHT)

anim_TEST_side_menu_breathe = Move_Rect(TEST_side_menu, (TEST_side_menu.x+200, TEST_side_menu.y), 1, ease_type=easeInOutSine, loop=ping_pong)
anim_TEST_side_menu_scale   = Scale_Rect(TEST_side_menu, (0.5, 0.5), 1, along_center=True, ease_type=easeInOutSine, loop=ping_pong)

# --------- end game options ---------
play_again_btn   = Button(screen, 250, 60, (255, SCREEN_HEIGHT//2 + 120), 5, None, text='Play Again', fontsize=26)
back_to_menu_btn = Button(screen, 250, 60, (545, SCREEN_HEIGHT//2 + 120), 5, None, text='Back to Main Menu', fontsize=18)

# --------- fade screen object ---------
screen_copy = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
fade_screen = Fade(screen, screen_copy, pygame.Color(OAR_BLUE), (SIDE_MENU_RECT_CURRENT.width + (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/11, 0), speed=25)

# --------- Sliders --------- 
slider_color = (65, 87, 110)
music_slider = Slider(screen, slider_color, (int(SIDE_MENU_RECT_CURRENT.width + (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/2.5), int(SCREEN_HEIGHT/1.75)), int(SCREEN_WIDTH*0.3), 5, border_radius=8, circle_x=MUSIC_VOLUME)
sound_slider = Slider(screen, slider_color, (int(SIDE_MENU_RECT_CURRENT.width + (SCREEN_WIDTH-SIDE_MENU_RECT_CURRENT.width)/2.5), int(SCREEN_HEIGHT/1.50)), int(SCREEN_WIDTH*0.3), 5, border_radius=8, circle_x=SOUND_VOLUME)

# --------- Sidebar objects --------- 
sidebar = Sidebar(screen, (0, 0), SIDE_MENU_RECT_DEFAULT.w, SIDE_MENU_RECT_DEFAULT.h)

def main_menu():



    pygame.mixer.music.load('audio/DamPy.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(MUSIC_VOLUME)

    full_trans_reset()
    game.reset()
    
    anim_title_breathe.play()
    # anim_title_squeeze.play()
    # anim_title_rotate.play()
    
    anim_TEST_side_menu_scale.play()
    anim_TEST_side_menu_breathe.play()

    while True:
        
        screen.fill(OAR_BLUE)
        
        screen.blit(title_surface, (((SCREEN_WIDTH-sidebar.sidebar_rect.w)//2)+
                    sidebar.sidebar_rect.w-title_surface.get_width()//2, 0))
        title_surface.fill(OAR_BLUE)

        # pygame.draw.rect(screen, BLACK, TEST_side_menu)
        sidebar_display(main_menu)
        title.display()

        if chip_animation:
            for i in range(len(red_chips)):
                red_chips[i].next_frame()
                blue_chips[i].next_frame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   

            # Debug
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game('Classic')
                    break

        anim_title_breathe.update()
        anim_title_squeeze.update()
        anim_title_rotate.update()
        # anim_TEST_side_menu_scale.update()
        # anim_TEST_side_menu_breathe.update()
        
        pygame.display.update()
        clock.tick(FPS)     

def title_up_display():
    """
    For moving the title img up + fade animation 
    """
    title_surface.fill(OAR_BLUE)
    title_surface.set_colorkey(OAR_BLUE)
    anim_title_up.update()
    if anim_title_up.IsFinished:
        fade_screen.full_fade()  
    title.display()
    screen.blit(title_surface, (((SCREEN_WIDTH-sidebar.sidebar_rect.w)//2)+
            sidebar.sidebar_rect.w-title_surface.get_width()//2, 0))

added = False
def sidebar_display(func_called):
    global added
    if not added:
        sidebar.add_option(2, "sb_play", pos=(SIDE_MENU_RECT_ACTIVE.width/8, 
                        side_menu_surface.get_height()/2.5+mainmenu_opt_gap*0.15), text='Play', description='Play Damath!',
                        target=select_mode)
        sidebar.add_option(2, "sb_online", pos=(SIDE_MENU_RECT_ACTIVE.width/8, 
                        side_menu_surface.get_height()/2.5+(1*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                        text='Online', description='Play Online!', target=online_menu)
        sidebar.add_option(2, "sb_help", pos=(SIDE_MENU_RECT_ACTIVE.width/8, 
                        side_menu_surface.get_height()/2.5+(2*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                        text='Help', description='Learn Damath!', target=help_menu)
        sidebar.add_option(2, "sb_options", pos=(SIDE_MENU_RECT_ACTIVE.width/8, 
                        side_menu_surface.get_height()/2.5+(3*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                        text='Options', description='Adjust to your preferences!', target=options_menu)
        sidebar.add_option(2, "sb_exit", pos=(SIDE_MENU_RECT_ACTIVE.width/8, 
                        side_menu_surface.get_height()/2.5+(4*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                            text='Exit', description='Quit the game... :<', target=sys.exit)
        added = True

    target_functions = {
        "sb_play": select_mode,
        "sb_online": online_menu,
        "sb_help": help_menu,
        "sb_options": options_menu,
        "sb_exit": sys.exit
    }

    for id in target_functions.keys():
        if target_functions[id] == func_called:
            target_functions[id] = None
            sidebar.get_option(id).target = None
        else:
            sidebar.get_option(id).target = target_functions[id]

    mx, my = pygame.mouse.get_pos() # gets the curent mouse position
    if sidebar.sidebar_rect.collidepoint((mx, my)):
        sidebar.set(state=HOVERED)
        for opt in sidebar.options.keys():
            if sidebar.get_option(opt).get_rect().collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    sidebar.update_options_state(opt, SELECTED)
                    sidebar.get_option(opt).call_target()
                else:
                    sidebar.update_options_state(opt, HOVERED)
            else:
                if sidebar.get_option(opt).state != SELECTED:
                    sidebar.update_options_state(opt, NORMAL)
    else:
        sidebar.set(state=NORMAL)
    screen.blit(LOGO, (sidebar.sidebar_rect.width/2 - LOGO.get_width()/2, side_menu_surface.get_height()*0.075))
    fade_screen.change_pos((sidebar.sidebar_rect.width, 0))

# --------- button collision detection function ---------

def btn_collided(x, y):
    buttons = [key for key in toggle_btn.keys()]

    for btn in buttons:
        if btn.btn_rect.collidepoint((x, y)):
            btn.toggled = not btn.toggled
        if btn.toggled:
            btn.set_state(btn.Toggled)
            start_select_btn.set_target(btn.get_target())
            start_select_btn.set_args(btn.get_args())
            for rembtn in buttons:
                if rembtn != btn and rembtn.toggled:
                    rembtn.toggled = not rembtn.toggled
                    rembtn.set_state(btn.Normal)
        else:
            btn.set_state(btn.Normal)
    

    # check if there aren't any toggled buttons
    if not any(btn.toggled for btn in buttons):
        start_select_btn.set_target(None)
        start_select_btn.set_args(None)

# --------- select mode function ---------

def select_mode():
    fade_screen.reset()

    classic_btn.set_target(start_game)
    speed_btn.set_target(start_game)
    running = True
    anim_title_up.play()

    while running:
    
        screen.fill(OAR_BLUE)
        sidebar_display(select_mode)

        if fade_screen.finished:
            screen.blit(font.render('Modes', True, WHITE), 
                                (sidebar.sidebar_rect.width + 
                                (SCREEN_WIDTH-sidebar.sidebar_rect.width)/11, 
                                SCREEN_HEIGHT/2.5))
            classic_btn.draw((sidebar.sidebar_rect.width + 
                                (SCREEN_WIDTH-sidebar.sidebar_rect.width)/10, 
                                SCREEN_HEIGHT/2))
            speed_btn.draw((((sidebar.sidebar_rect.width + 
                                (SCREEN_WIDTH-sidebar.sidebar_rect.width)/10 + 
                                btn_size[0])+(sidebar.sidebar_rect.width + 
                                (SCREEN_WIDTH-sidebar.sidebar_rect.width) - 
                                (SCREEN_WIDTH-sidebar.sidebar_rect.width)/10 - 
                                btn_size[0]))/2 - btn_size[0]/2, SCREEN_HEIGHT/2))
            custom_btn.draw(((sidebar.sidebar_rect.width + 
                                (SCREEN_WIDTH-sidebar.sidebar_rect.width) - 
                                (SCREEN_WIDTH-sidebar.sidebar_rect.width)/10 - 
                                btn_size[0]), SCREEN_HEIGHT/2))
            start_select_btn.draw(((sidebar.sidebar_rect.width + 
                                SCREEN_WIDTH)/2 - btn_size[0]//2, 
                                SCREEN_HEIGHT/1.25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if event.button == 1:
                    if start_select_btn.btn_rect.collidepoint((x, y)):
                        try:
                            start_select_btn.set_state(start_select_btn.Selected)
                            start_select_btn.call_target()
                        except:
                            continue
                    else:
                        btn_collided(x, y)

        title_up_display()
        pygame.display.update()
        clock.tick(FPS)

# --------- online menu function ---------

def online_menu():

    fade_screen.reset()
    anim_title_up.play()
    running = True
    
    while running:

        screen.fill(OAR_BLUE)

        mx, my = pygame.mouse.get_pos()
        sidebar_display(online_menu)

        if fade_screen.finished:
            screen.blit(font.render('Online', True, WHITE), 
                        (sidebar.sidebar_rect.width + 
                        (SCREEN_WIDTH-sidebar.sidebar_rect.width)/11, 
                        SCREEN_HEIGHT/2.5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        title_up_display()
        pygame.display.update()
        clock.tick(FPS)

# --------- help menu function ---------

def help_menu():

    fade_screen.reset()
    anim_title_up.play()
    running = True

    t1_rectwin = create_window(screen, (500, 350),200, 300, DARK_BLUE)
    t2_rectwin = create_window(screen, (750, 350), 200, 100, PERSIMMON_ORANGE, border_radius=8, border_thickness=2)
    t3_rectwin = create_window(screen, (1000, 350), 200, 100, DARK_ORANGE, border_thickness=10)
    t4_rectwin = create_window(screen, (750, 475), 475, 175, DARK_BLUE, border_thickness=16) 

    while running:
        screen.fill(OAR_BLUE)

        mx, my = pygame.mouse.get_pos()
        sidebar_display(help_menu)

        if fade_screen.finished:
            screen.blit(font.render('Help', True, WHITE), 
                        (sidebar.sidebar_rect.width + 
                        (SCREEN_WIDTH-sidebar.sidebar_rect.width)/11, 
                        SCREEN_HEIGHT/2.5))
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        t1_rectwin.draw()
        t2_rectwin.draw()
        t3_rectwin.draw()
        t4_rectwin.draw()
        title_up_display()
        pygame.display.update()
        clock.tick(FPS)

# --------- options menu function ---------

def options_menu():
    
    options_font = pygame.font.Font('font\CookieRun_Regular.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.06))
    fade_screen.reset()
    anim_title_up.play()
    global MUSIC_VOLUME, SOUND_VOLUME
    running = True
    
    while running:
        screen.fill(OAR_BLUE)

        mx, my = pygame.mouse.get_pos()
        sidebar_display(options_menu)

        if fade_screen.finished:
            screen.blit(font.render('Options', True, WHITE), 
                        (sidebar.sidebar_rect.width + 
                        (SCREEN_WIDTH-sidebar.sidebar_rect.width)/11, 
                        SCREEN_HEIGHT/2.5))
            music_slider.draw(int(sidebar.sidebar_rect.width + 
                            (SCREEN_WIDTH-sidebar.sidebar_rect.width)/2.5))
            sound_slider.draw(int(sidebar.sidebar_rect.width + 
                            (SCREEN_WIDTH-sidebar.sidebar_rect.width)/2.5))
            screen.blit(options_font.render('Music', True, WHITE), 
                        (int(sidebar.sidebar_rect.width + 
                        (SCREEN_WIDTH-sidebar.sidebar_rect.width)/4.65),
                        int(SCREEN_HEIGHT/1.75 - music_slider.height*6)))
            screen.blit(options_font.render('SFX', True, WHITE), 
                        (int(sidebar.sidebar_rect.width + 
                        (SCREEN_WIDTH-sidebar.sidebar_rect.width)/4.65), 
                        int(SCREEN_HEIGHT/1.50 - music_slider.height*6)))

            if not sound_slider.get_slider_state() and music_slider.get_collider().collidepoint((mx, my)):
                music_slider.update(mx)
                MUSIC_VOLUME = music_slider.get_value()/100
                pygame.mixer.music.set_volume(MUSIC_VOLUME)

            elif not music_slider.get_slider_state() and sound_slider.get_collider().collidepoint((mx, my)):
                sound_slider.update(mx)
                SOUND_VOLUME = sound_slider.get_value()/100
                change_volume(SOUND_VOLUME)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        title_up_display()
        pygame.display.update()
        clock.tick(FPS)

# --------- pause function ---------

def pause():
    paused = True
    full_trans_reset()

    restart_play_trans = False
    pause_play_trans = False

    while paused:
        screen.fill(OAR_BLUE)
        screen.blit(TITLE_BG, (0, 0))

        if chip_animation:
            if game.turn == RED:
                big_red_chip.play()
            else:
                big_blue_chip.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    paused = not paused
                    break

        mx, my = pygame.mouse.get_pos() # gets the curent mouse position
        #print(mx, my)
      
        if resume_btn.top_rect.collidepoint((mx, my)):
            resume_btn.hover_update(start_game)
            restart_btn.reset()
            pause_options_btn.reset()
            quit_btn.reset()
        elif restart_btn.top_rect.collidepoint((mx, my)):
            restart_btn.hover_update()
            pause_options_btn.reset()
            quit_btn.reset()
            if pygame.mouse.get_pressed()[0]:
                restart_play_trans = True
                game.reset()
        elif pause_options_btn.top_rect.collidepoint((mx, my)):
            pause_options_btn.hover_update(options_menu, param='pause')
            resume_btn.reset()
            restart_btn.reset()
            quit_btn.reset()
        elif quit_btn.top_rect.collidepoint((mx, my)):
            resume_btn.reset()
            restart_btn.reset()
            pause_options_btn.reset()   
            quit_btn.hover_update()  
            if pygame.mouse.get_pressed()[0]:
                pygame.mixer.music.play(-1)
                pause_play_trans = True 
        else:
            quit_btn.reset()
            resume_btn.reset()
            restart_btn.reset()
            pause_options_btn.reset()           

        #pygame.draw.rect(paused_surface, BLACK, (0, 0, paused_rect.w, paused_rect.h), border_radius=25)
        
        resume_btn.draw()
        restart_btn.draw()
        pause_options_btn.draw()
        quit_btn.draw() 

        if restart_play_trans or pause_play_trans:
            transition_in.play()
            if transition_in.get_finished():
                if restart_play_trans:
                    start_game()
                else:
                    main_menu()

        pygame.display.update()
        clock.tick(FPS)

def timer_thread():

    global thread_running
    turn_timer.reset()
    global_timer.reset()

    thread_running = True
    
    while thread_running:
        time.sleep(0.1)
        #print(turn_timer.remaining_time)
        turn_timer.start_timer()
        global_timer.start_timer()
        
        if turn_timer.starttime_started:
            if turn_timer.remaining_time >= 0:
                turn_timer.remaining_time = turn_timer.endtime - turn_timer.currenttime
            else:
                game.change_turn()

        if global_timer.starttime_started:
            if ceil(global_timer.remaining_time) >= 0:
                global_timer.remaining_time = global_timer.endtime - global_timer.currenttime
            else:
                thread_running = False
                return
    return
        
start_game_running = True
thread_running = True

# --------- start game function ---------
# (when Start button is pressed)

def start_game(mode):

    global thread_running

    if mode == 'Classic':
        turn_timer.set_duration(60)
        global_timer.set_duration(1200)
    elif mode == 'Speed':
        turn_timer.set_duration(15)
        global_timer.set_duration(300)

    text_mode = font_cookie_run_reg.render(str(mode), True, OAR_BLUE)
    TIMERTHREAD = threading.Thread(target=timer_thread)

    print(f'[MODE]: {mode}')
    start_game_running = True

    pygame.mixer.music.stop()
    full_trans_reset()

    while start_game_running:

        if TIMER:
            if not TIMERTHREAD.is_alive():
                TIMERTHREAD.start() 

        mins, secs = global_timer.get_remaining_time()
        global_timer_text = font_cookie_run_reg.render(str(f'{mins:02d}:{secs:02d}'), True, WHITE)

        change_volume(SOUND_VOLUME)
        #screen.blit(CLEAR_BG, (0, 0)) 
        screen.fill(OAR_BLUE)    
        screen.blit(side_menu_surface, (0, 0))
        side_menu_surface.fill(DARK_GRAY_BLUE)      
        
        if game.winner() != None:
            print(game.winner()) 
            start_game_running = False
            thread_running = False
            game_ends()
            
        # Get current mouse position
        m_pos = pygame.mouse.get_pos()

        if return_btn.top_rect.collidepoint(m_pos):
            return_btn.hover_update(pause, _fade=False)
        else:
            return_btn.reset()

        screen.blit(game_side_surface, (0, 0))
        game_side_surface.fill(DARK_GRAY_BLUE)
        
        screen.blit(board_area_surface, (game_side_surface.get_width(), 0))
        board_area_surface.fill(OAR_BLUE)

        # damath_board_shadow.display()
        damath_board.display()

        # Renders chips
        board_area_surface.blit(chips_surface, (tiles_rect))
        
        # Render captured pieces
        board_area_surface.blit(p1_captured_pieces_surface, (p1_captured_pieces_rect))
        board_area_surface.blit(p2_captured_pieces_surface, (p2_captured_pieces_rect))
        p1_captured_pieces_surface.fill(OAR_BLUE)
        p2_captured_pieces_surface.fill(OAR_BLUE)
        
        # Display side bar elements
        mini_title.display()

        screen.blit(text_scores,
                    (game_side_surface.get_width()//2-text_scores.get_width()//2, game_side_surface.get_height()*0.2))

        screen.blit(global_timer_text,
                    (game_side_surface.get_width()//2-global_timer_text.get_width()//2, game_side_surface.get_height()*0.825)) 

        screen.blit(text_mode,
                    (game_side_surface.get_width()//2-text_mode.get_width()//2, game_side_surface.get_height()*0.9))

        if CHEATS:
            cheats.draw()

            if cheats.ShowWindow:
                if cheats.window.get_rect().collidepoint(m_pos):
                    cheats.check_for_hover(m_pos, cheats.window.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start_game_running = False
                thread_running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    pause()
                    break
            # cheat codes
                if CHEATS:
                    _keys = pygame.key.get_pressed()
                    
                    if _keys[pygame.K_LCTRL]:

                        if _keys[pygame.K_w]: # king pieces

                            if _keys[pygame.K_1]: # blue pieces
                                drow, dcol = get_row_col_from_mouse(pygame.mouse.get_pos())
                                piece = game.board.get_piece(drow, dcol)
                                if dcol % 2 == 1:
                                    if drow % 2 == 1:
                                        if piece.color == RED:
                                            game.board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            game.board.board[drow][dcol].king = True
                                            game.board.red_left -= 1
                                            game.board.white_left += 1
                                        elif piece.color == 0:
                                            game.board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            game.board.board[drow][dcol].king = True
                                            game.board.white_left += 1                                 
                                else:
                                    if drow % 2 == 0:
                                        if piece.color == RED:
                                            game.board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            game.board.board[drow][dcol].king = True
                                            game.board.red_left -= 1
                                            game.board.white_left += 1
                                        elif piece.color == 0:
                                            game.board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            game.board.board[drow][dcol].king = True
                                            game.board.white_left += 1  

                            if _keys[pygame.K_2]: # red pieces
                                drow, dcol = get_row_col_from_mouse(pygame.mouse.get_pos())
                                piece = game.board.get_piece(drow, dcol)
                                if dcol % 2 == 1:
                                    if drow % 2 == 1:
                                        if piece.color == LIGHT_BLUE:
                                            game.board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            game.board.board[drow][dcol].king = True
                                            game.board.red_left += 1
                                            game.board.white_left -= 1
                                        elif piece.color == 0:
                                            game.board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            game.board.board[drow][dcol].king = True
                                            game.board.red_left += 1                                 
                                else:
                                    if drow % 2 == 0:
                                        if piece.color == LIGHT_BLUE:
                                            game.board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            game.board.board[drow][dcol].king = True
                                            game.board.red_left += 1
                                            game.board.white_left -= 1
                                        elif piece.color == 0:
                                            game.board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            game.board.board[drow][dcol].king = True
                                            game.board.red_left += 1  

                        elif _keys[pygame.K_1]: # add normal blue piece
                            drow, dcol = get_row_col_from_mouse(pygame.mouse.get_pos())
                            piece = game.board.get_piece(drow, dcol)
                            if dcol % 2 == 1:
                                if drow % 2 == 1:
                                    if piece.color == RED:
                                        game.board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                        game.board.red_left -= 1
                                        game.board.white_left += 1
                                    elif piece.color == 0:
                                        game.board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                        game.board.white_left += 1                                 
                            else:
                                if drow % 2 == 0:
                                    if piece.color == RED:
                                        game.board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                        game.board.red_left -= 1
                                        game.board.white_left += 1
                                    elif piece.color == 0:
                                        game.board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                        game.board.white_left += 1  

                        elif _keys[pygame.K_2]: # add normal red piece
                            drow, dcol = get_row_col_from_mouse(pygame.mouse.get_pos())
                            piece = game.board.get_piece(drow, dcol)
                            if dcol % 2 == 1:
                                if drow % 2 == 1:
                                    if piece.color == LIGHT_BLUE:
                                        game.board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                        game.board.red_left += 1
                                        game.board.white_left -= 1
                                    elif piece.color == 0:
                                        game.board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                        game.board.red_left += 1                                 
                            else:
                                if drow % 2 == 0:
                                    if piece.color == LIGHT_BLUE:
                                        game.board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                        game.board.red_left += 1
                                        game.board.white_left -= 1
                                    elif piece.color == 0:
                                        game.board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                        game.board.red_left += 1

                    if _keys[pygame.K_LSHIFT]:
                        if _keys[pygame.K_c]: # change turn
                            game.change_turn()
                        if _keys[pygame.K_1]: # game resets
                            game.reset()
                        if _keys[pygame.K_2]: # blue wins
                            game.scoreboard.p1_score = 1
                            game.scoreboard.p2_score = 0
                            game.board.orange_pieces_count = 0
                        if _keys[pygame.K_3]: # red wins
                            game.scoreboard.p1_score = 0
                            game.scoreboard.p2_score = 1
                            game.board.blue_pieces_count = 0
                        if _keys[pygame.K_4]: # make all pieces king
                            for i in range(8):
                                for j in range(8):
                                    game.board.board[i][j].IsKing = True
                        if _keys[pygame.K_5]: # make all pieces not king
                            for i in range(8):
                                for j in range(8):
                                    game.board.board[i][j].IsKing = False   
                        if _keys[pygame.K_6]: # removes all pieces
                            for i in range(8):
                                for j in range(8):
                                    game.board.board[i][j] = Piece(chips_surface, i, j, 0, 0)
                        if _keys[pygame.K_7]: # displays a single chip in both ends
                            for i in range(8):
                                for j in range(8):
                                    game.board.board[i][j] = Piece(chips_surface, i, j, 0, 0)
                            game.board.board[0][2] = Piece(chips_surface, 0, 2, PLAYER_TWO, 2)   
                            game.board.board[7][7] = Piece(chips_surface, 7, 7, PLAYER_ONE, 2)  
                            game.board.red_left = 1
                            game.board.white_left = 1
                        if pygame.mouse.get_pressed()[2]: #removes the piece
                            drow, dcol = get_row_col_from_mouse(pygame.mouse.get_pos())
                            piece = [game.board.get_piece(drow, dcol)]
                            game.board.move_to_graveyard(piece)

                    if _keys[pygame.K_m]:
                        if _keys[pygame.K_0]:
                            game.set_mode('Naturals')
                        elif _keys[pygame.K_1]:
                            game.set_mode('Integers')
                        elif _keys[pygame.K_2]:
                            game.set_mode('Rationals')
                        elif _keys[pygame.K_3]:
                            game.set_mode('Radicals')
                        elif _keys[pygame.K_4]:
                            game.set_mode('Polynomials')

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Left click
                if pygame.mouse.get_pressed()[0]:
                    
                    if board_rect.collidepoint(m_pos):
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        
                        if game.moved_piece != None:
                            if row != game.moved_piece.row or row != game.moved_piece.col:
                                INVALID_SOUND.play()

                        if cheats.ShowWindow:
                            if CHEATS:
                                if cheats.window.get_rect().collidepoint(m_pos):
                                    cheats.invoke()
                        else:
                            if (-1 < row < ROWS) and (-1 < col < COLS):
                                game.select(row, col)
                                
                        cheats.ShowWindow = False

                if CHEATS:
                    if pygame.mouse.get_pressed()[2]:
                        # Right click
                        row, col = get_row_col_from_mouse(m_pos)

                        if (-1 < row < ROWS) and (-1 < col < COLS):
                            cheats.create_window(m_pos, row, col)
                        else:
                            cheats.create_window(m_pos, row, col, OnBoard=False)


                    

        # game_side_surface.blit(scoreboard_surface, (scoreboard_rect))
        # screen.blit(scoreboard_surface, (scoreboard_rect.x, scoreboard_rect.y))
        # scoreboard.draw()
        # game.board.update_theme(themes.list[themes.focused].board)
        # transition_out.play() 

        # return_btn.display_image() 
        game.update()
        pygame.display.update()
        clock.tick(FPS)
 
# --------- themes menu function ---------

def themes_menu(caller=None):
    
    running = True

    while running:

        screen.fill(OAR_BLUE)
        screen.blit(CLEAR_BG, (0, 0))

        for idx, theme in enumerate(themes.list):
            themes.rect_list[idx] = pygame.Rect(theme.x, theme.y, theme.theme.get_width(), theme.theme.get_height())

        if chip_animation:
            for i in range(3):
                red_chips[i].next_frame()
                blue_chips[i].next_frame()
        
        mx, my = pygame.mouse.get_pos() # gets the curent mouse position

        themes.display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.display.update()
                
                if event.key == pygame.K_LEFT:
                    themes.move('right')

                if event.key == pygame.K_RIGHT:
                    themes.move('left')

                if event.key == pygame.K_RETURN:
                    THEME_SELECTED_SOUND.play()
                    game.board.update_theme(themes.list[themes.focused].board)
                    if 'main' == caller:
                        main_menu()
                    elif 'pause' == caller:
                        pause()                    

            if event.type == pygame.MOUSEBUTTONDOWN:
                if themes.focused < len(themes.rect_list)-1:
                    if themes.rect_list[themes.focused+1].collidepoint((mx, my)):
                        if pygame.mouse.get_pressed()[0]:
                            themes.move('left')
                if themes.focused > 0:
                    if themes.rect_list[themes.focused-1].collidepoint((mx, my)):
                        if pygame.mouse.get_pressed()[0]:
                            themes.move('right')

        # if return_btn.top_rect.collidepoint((mx, my)):
        #     if 'main' is who_called_me:
        #         return_btn.hover_update(main_menu)
        #     elif 'pause' is who_called_me:
        #         return_btn.hover_update(start_game)

        # elif themes.rect_list[themes.focused].collidepoint((mx, my)):
        #     return_btn.reset()
        #     if pygame.mouse.get_pressed()[0]:
        #         THEME_SELECTED_SOUND.play()
        #         game.board.update_theme(themes.list[themes.focused].board)
        #         if 'main' is who_called_me:
        #             main_menu()
        #         elif 'pause' is who_called_me:
        #             pause()
        else:
            return_btn.reset()

        return_btn.display_image()        
        pygame.display.update()
        clock.tick(FPS)

# --------- game end function ---------
def game_ends():

    pygame.mixer.music.load('audio\\ROUTE_209.wav')
    pygame.mixer.music.play()
    winner_anim_frames = []

    # only load the frames of the winning color
    print(game.winner() == RED)

    if game.winner() == RED:
        for i in range(21):
            frame = pygame.transform.smoothscale(pygame.image.load(f'assets\win\RED_WINS\{i+18}.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
            winner_anim_frames.append(frame)
    else:
        for i in range(20):
            frame = pygame.transform.smoothscale(pygame.image.load(f'assets\win\BLUE_WINS\{i+39}.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
            winner_anim_frames.append(frame)

    WINNER = WinnerWindow(screen, winner_anim_frames)
    WINNER.set_delay(60) # winner window will appear after 60 / fps (1 sec)

    play_again_transition_in = False
    back_to_menu_transition_in = False
    running = True
    
    while running:

        screen.blit(CLEAR_BG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        WINNER.delay_start()
        if WINNER.delay_finished:
            WINNER.play()
        
        if WINNER.finished:
            show_score()
            play_again_btn.draw()
            back_to_menu_btn.draw()

            mx, my = pygame.mouse.get_pos()

            if play_again_btn.top_rect.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    play_again_transition_in = True
                back_to_menu_btn.reset()
                play_again_btn.hover_update()
            elif back_to_menu_btn.top_rect.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    back_to_menu_transition_in = True
                play_again_btn.reset()
                back_to_menu_btn.hover_update()
            else:
                play_again_btn.reset()
                back_to_menu_btn.reset()

            if play_again_transition_in:
                transition_in.play()
                if transition_in.get_finished():
                    pygame.mixer.music.stop()
                    game.reset()
                    running = False
                    start_game()
            
            if back_to_menu_transition_in:
                transition_in.play()
                if transition_in.get_finished():
                    pygame.mixer.music.stop()
                    running = False
                    main_menu()

            WINNER.reset()

        pygame.display.update()
        clock.tick(FPS)


class WinnerWindow:
    def __init__ (self, screen, frames_list):
        self.screen = screen
        self.frame = 0
        self.finished = False
        
        self.sound_played = False
        self.delay = 0
        self.delay_time = 0
        self.delay_finished = False
        self.frames_list = frames_list
        self.y = 0

    def play(self):
        if not self.sound_played:
            self.sound_played = True

        if not self.finished:
            if self.frame == len(self.frames_list)-1:
                self.finished = True
            else:
                self.frame += 1
            self.screen.blit(self.frames_list[self.frame], (0, 0))

    def set_delay(self, time):
        self.delay = time

    def delay_start(self):
        if not self.delay_finished:
            if self.delay != self.delay_time:
                self.delay_time+=1
            elif self.delay == self.delay_time:
                self.delay_finished = True
    
    def reset(self):
        self.finished = False
        self.delay_time = 0
        self.sound_played = False

main_menu()