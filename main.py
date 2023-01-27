# 
# Damath
# 

import pygame 
import sys
import random 
import threading
from copy import copy
from console import DeveloperConsole
from math import ceil
from damath.actions import Actions
from damath.board import *
from damath.cheats import Cheats
from damath.game import *
from damath.piece import Piece
from damath.ruleset import Ruleset
from damath.scoreboard import Scoreboard
from damath.constants import *
from damath.timer import *
from display_constants import *
from event_loop import event_loop
import screens.sidebar_display
from screens.select_mode import SelectModeScreen
from screens.multi_menu import MultiMenuScreen
from screens.help_menu import HelpMenuScreen
from screens.options_menu import OptionsMenuScreen
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
from ui_class.mode_window import *
from queue import Queue
# Multiplayer
from audio_constants import * 
from objects import *
from assets import *
from options import *

# --------- initialization ---------
pygame.init()
pygame.font.init()
pygame.mixer.init(44100, -16, 2, 2048)

# --------- custom cursor ---------
pygame.mouse.set_visible(False)

# --------- defining constants / objects for screen  ---------

ANIM_SPEED  = 20
ANIM_ALPHA  = 255
CHIP_WIDTH  = 360
CHIP_HEIGHT = 240

clock = pygame.time.Clock()
font  = pygame.font.Font('font\CookieRun_Bold.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.05))    

# --------- piece move function ---------
def get_cell_from_mouse(pos):
    x, y = pos
    col = (x - selection_guide_rect.w) // square_size
    row = abs(((y - selection_guide_rect.h) // square_size) - 7)

    if enableDebugMode:
        print(f"[Debug/Action]: Clicked on cell ({col}, {row})")
    return col, row

def get_cell_from_mouse_raw(pos):
    """
    Returns a cell (column and row) from the board based from mouse position.
    Returns a negative value if out of bounds of the board.
    """
    
    x, y = pos
    col = (x - selection_guide_rect.w) // square_size
    row = (y - selection_guide_rect.h) // square_size

    if enableDebugMode:
        print(f"[Debug/Action]: Clicked on cell ({col}, {row}), raw")

    if col < 0 or col > 7:
        return -1, -1
    if row < 0 or row > 7:
        return -1, -1

    return col, row

def anim_dim():
    return random.randrange(0-CHIP_WIDTH, SCREEN_WIDTH, 1), 0-CHIP_HEIGHT

def show_score():   
    score = round(max(game.scoreboard.score()), 2)
    font = pygame.font.Font('font\CookieRun_Bold.ttf', 100).render(str(score), True, WHITE)
    #score_rect = pygame.Rect(255, 165, 535, 235)
    screen.blit(font, (SCREEN_WIDTH//2 - font.get_width()//2 - 12, SCREEN_HEIGHT//(2.8)))

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

# BOARDS = [BOARD_BLACK,   BOARD_GREEN, 
#           BOARD_BROWN,   BOARD_LIGHTBROWN,
#           BOARD_PINK,    BOARD_BROWN_2, 
#           BOARD_BROWN_3, BOARD_BLUE, 
#           BOARD_RED,     BOARD_COCO_MARTHEME]

# for idx, board in enumerate(BOARDS):
#     themes.append(Themes(screen, board, idx))

# BOARD_DEFAULT_THEME = themes.list[themes.focused].board #black board
BOARD_DEFAULT_THEME = BOARD_BLACK

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
game = Match(chips_surface, board, scoreboard, BOARD_DEFAULT_THEME)


if chip_animation:  
    big_blue_chip = SpinningChip(screen, 'blue')
    big_red_chip  = SpinningChip(screen, 'red')

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


# --------- Side menu rect tweenable --------- 

TEST_side_menu = pygame.Rect(0, 0, SCREEN_WIDTH*0.15, SCREEN_HEIGHT)

anim_TEST_side_menu_breathe = Move_Rect(TEST_side_menu, (TEST_side_menu.x+200, TEST_side_menu.y), 1, ease_type=easeInOutSine, loop=ping_pong)
anim_TEST_side_menu_scale   = Scale_Rect(TEST_side_menu, (0.5, 0.5), 1, along_center=True, ease_type=easeInOutSine, loop=ping_pong)

# --------- end game options ---------
play_again_btn   = Button(screen, 250, 60, (255, SCREEN_HEIGHT//2 + 120), 5, None, text='Play Again', fontsize=26)
back_to_menu_btn = Button(screen, 250, 60, (545, SCREEN_HEIGHT//2 + 120), 5, None, text='Back to Main Menu', fontsize=18)

# Decluttered menu functions, but Sidebar needs to be fixed to 
# avoid unnecessary function declarations just to maintain sidebar option's stored functions
# since it gets removed everytime a function calls it to avoid recursion error
def _select_mode():
    sidebar.set_target([_select_mode, _multi_menu, _help_menu, _options_menu, _exit])
    start_select_btn.set_target(Main.create_and_start_match)
    select_mode_screen.start()

def _multi_menu():
    sidebar.set_target([_select_mode, _multi_menu, _help_menu, _options_menu, _exit])
    multi_menu_screen.start()

def _help_menu():
    sidebar.set_target([_select_mode, _multi_menu, _help_menu, _options_menu, _exit])
    help_menu_screen.start()

def _options_menu():
    sidebar.set_target([_select_mode, _multi_menu, _help_menu, _options_menu, _exit])
    options_menu_screen.start()

def _exit():
    sys.exit()

#TODO: Needs refactoring in Sidebar
sidebar.add_option(3, "sb_play", pos=(SIDE_MENU_RECT_ACTIVE.width/4, 
                side_menu_surface.get_height()/2.5+mainmenu_opt_gap*0.15), text='Play', description='Play Damath!',
                icon=play_icon, target=_select_mode)
sidebar.add_option(3, "sb_online", pos=(SIDE_MENU_RECT_ACTIVE.width/4, 
                side_menu_surface.get_height()/2.5+(1*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                text='Multi', description='Play with friends!', 
                icon=online_icon, target=_multi_menu)
sidebar.add_option(3, "sb_help", pos=(SIDE_MENU_RECT_ACTIVE.width/4, 
                side_menu_surface.get_height()/2.5+(2*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                text='Help', description='Learn Damath!', 
                icon=help_icon, icon_offset=55, target=_help_menu)
sidebar.add_option(3, "sb_options", pos=(SIDE_MENU_RECT_ACTIVE.width/4, 
                side_menu_surface.get_height()/2.5+(3*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                text='Options', description='Adjust to your preferences!', 
                icon=option_icon, target=_options_menu)
sidebar.add_option(3, "sb_exit", pos=(SIDE_MENU_RECT_ACTIVE.width/4, 
                side_menu_surface.get_height()/2.5+(4*mainmenu_opt_gap+mainmenu_opt_gap*0.15)),
                    text='Exit', description='Quit the game... :<', 
                    icon=exit_icon, target=_exit)

sidebar.set_target([_select_mode, _multi_menu, _help_menu, _options_menu, sys.exit])

select_mode_screen = SelectModeScreen(screen, bg_color=OAR_BLUE, target=_select_mode)
multi_menu_screen = MultiMenuScreen(screen, bg_color=OAR_BLUE, target=_multi_menu)
help_menu_screen = HelpMenuScreen(screen, bg_color=OAR_BLUE, target=_help_menu)
options_menu_screen = OptionsMenuScreen(screen, bg_color=OAR_BLUE, target=_options_menu)

# --------- pause function ---------

def pause(mode):
    global thread_running, paused
    paused = True

    turn_timer.pause()
    global_timer.pause()

    # a function to break the while loop since
    # "break" isn't a function in itself, and 
    # calling the previous caller function 
    # will reset the game / requires more modification
    # to create the desired behavior
    def unpause():
        global paused
        paused = False

    resume_btn.set_target(unpause)
    options_btn.set_target(mini_options)
    restart_btn.set_target(None)
    # restart_btn.set_target(game.reset)
    main_menu_btn.set_target(Main.title)

    while paused:

        screen.blit(side_menu_surface, (0, 0))
        side_menu_surface.fill(DARK_GRAY_BLUE) 

        screen.blit(game_side_surface, (0, 0))
        game_side_surface.fill(DARK_GRAY_BLUE)

        screen.blit(board_area_surface, (game_side_surface.get_width(), 0))
        board_area_surface.fill(OAR_BLUE)     
        damath_board.display()

        # Display side bar elements
        mini_title.display()

        screen.blit(text_scores,
                    (game_side_surface.get_width()//2-text_scores.get_width()//2, game_side_surface.get_height()*0.2))

        screen.blit(global_timer_text,
                    (game_side_surface.get_width()//2-global_timer_text.get_width()//2, game_side_surface.get_height()*0.825)) 

        screen.blit(text_mode,
                    (game_side_surface.get_width()//2-text_mode.get_width()//2, game_side_surface.get_height()*0.9))
    
        # overlays the semi-transparent surface
        screen.blit(alpha_surface, (0, 0))

        # displays the pause window elements
        pause_window.wupdate(x=SCREEN_WIDTH*0.5-pause_window.width*0.5, 
                        y=SCREEN_HEIGHT*0.5-pause_window.h*0.5)
        pause_window.draw()

        screen.blit(pause_text, (pause_window.x+(pause_window.w*0.5-
                            pause_text.get_width()*0.5), 
                            SCREEN_HEIGHT*0.25))
        
        pause_buttons_group.draw()

        for event in event_loop.get_event():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    turn_timer.resume()
                    global_timer.resume()
                    paused = not paused

        # the attribute pos_reset is checked to see
        # if the NButton object has been previously clicked 
        # and is now no longer clicked, which means the function
        # is already called and the pause window should now close
        # (used to prevent executing the function without the button 
        # behaving in its selected state first once clicked)
        if resume_btn.pos_reset:
            turn_timer.resume()
            global_timer.resume()

        if restart_btn.pos_reset:
            start_game(mode)

        screen.blit(CURSOR, pygame.mouse.get_pos())
        Main.Match.update() 
        pygame.display.update()
        clock.tick(FPS) 

def mini_options():
    option_font = pygame.font.Font('font/CookieRun_Bold.ttf', 120)
    option_text = option_font.render('NEEDS UI DESIGN >//<', True, WHITE)
    x = 0
    running = True
    while running:
        screen.fill(OAR_BLUE)
        screen.blit(pygame.transform.smoothscale_by(option_text, 4),
                        (SCREEN_WIDTH*0.5-
                    option_text.get_width()*0.5+x, 
                    SCREEN_HEIGHT*0.25))
        screen.blit(option_text, (SCREEN_WIDTH*0.5-
                    option_text.get_width()*0.5-x, 
                    SCREEN_HEIGHT*0.1))

        if x < 200:
            x+=1
        else:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        screen.blit(CURSOR, pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(FPS)
        
def timer_thread():

    global thread_running
    turn_timer.reset()
    global_timer.reset()

    thread_running = True

    turn_timer.start_timer()
    global_timer.start_timer()  

    while thread_running:
        time.sleep(0.1)
        #print(turn_timer.remaining_time)
        
        if turn_timer.starttime_started and turn_timer.is_running:
            turn_timer.update()
            if turn_timer.remaining_time >= 0:
                turn_timer.remaining_time = turn_timer.endtime - turn_timer.currenttime
            else:
                game.change_turn()

        if global_timer.starttime_started and global_timer.is_running:
            global_timer.update()
            if ceil(global_timer.remaining_time) >= 0:
                global_timer.remaining_time = global_timer.endtime - global_timer.currenttime
            else:
                thread_running = False
                return
    return
        
GameIsRunning = True
thread_running = True

# --------- start game function ---------
# (when Start button is pressed)
def start_game(mode, IsMultiplayer=False):
    pass

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
                    # Game.Board.update_theme(themes.list[themes.focused].board)
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
        #         Game.Board.update_theme(themes.list[themes.focused].board)
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

    if game.winner() == PLAYER_TWO:
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
                    Main.title()

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

class Damath:

    def __init__(self) -> None:
        self.Queue = Queue()
        self.Match = Match()

    def start(self):
        self.title()

    def title(self):
        """
        Launch Title Screen.
        """
        
        pygame.mixer.music.load('audio/DamPy.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)

        # full_trans_reset()
        # game.reset()

        anim_title_up.reset()
        anim_title_breathe.play()
        # anim_title_squeeze.play()
        # anim_title_rotate.play()
        
        anim_TEST_side_menu_scale.play()
        anim_TEST_side_menu_breathe.play()

        while True:
            try:
                _start_match = Main.Queue.get(False)
                _start_match()
            except: 
                pass

            screen.fill(OAR_BLUE)
            screen.blit(title_surface, (((SCREEN_WIDTH-sidebar.sidebar_rect.w) // 2) +
                        sidebar.sidebar_rect.w-title_surface.get_width() // 2, 0))
            title_surface.fill(OAR_BLUE)

            # pygame.draw.rect(screen, BLACK, TEST_side_menu)
            sidebar.display(None)
            screen.blit(LOGO, (sidebar.sidebar_rect.width/2 - LOGO.get_width()/2, side_menu_surface.get_height()*0.075))
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
                        Main.start_match('Classic')
                        return

                    if event.key == pygame.K_EQUALS:
                        Main.start_match('Classic')
                        return

                    if event.key == pygame.K_MINUS:
                        Main.start_match()
                        return
                    
                    if event.key == pygame.K_t:
                        _select_mode()
                        return

            anim_title_breathe.update()
            anim_title_squeeze.update()
            anim_title_rotate.update()
            # anim_TEST_side_menu_scale.update()
            # anim_TEST_side_menu_breathe.update()
            
            screen.blit(CURSOR, pygame.mouse.get_pos())
            pygame.display.update()
            clock.tick(FPS)     

    def create_match(self, mode: str) -> Match:
        """
        Creates a new match with specified mode.
        The created match is stored as the attribute "Damath.Match" and is overridden by succeeding created matches.
        A different instance of a match can also be created as the function returns a Match class.
        """

        # Create an instance of Rules first
        Rules = Ruleset()

        # For custom games
        # Call this if a toggleable is pressed
        # e.g. Promotion toggleable
        Rules.allowPromotion = not Rules.allowPromotion
        # or manual set
        Rules.allowCheats = True
        
        # For pre-defined modes
        Rules.set(mode)

        # MANUAL RULE SET FOR DEBUGGING
        Rules.allowActions = True
        Rules.allowCheats = True
        Rules.IsMultiplayer = True

        # Once Start is pressed, instantiate other major classes
        # This can be put inside a separate function, taking Rules as param
        Gameboard = Board() # The board is now referred to as the "Gameboard"
        Gameboard.surface = chips_surface
        Gameboard.init()

        Scores = Scoreboard()   # The scoreboard is now "Scoreboard"
        Scores.surface = game_side_surface
        Scores.init()

        Game = Match()  # The game (or "a single game") is now referred to as a "Match"
        Game.Surface = chips_surface
        Game.Board = Gameboard
        Game.Scores = Scores
        # Assign the modified ruleset to the "Game" class
        Game.Rules = Rules  
        Game.init()
        
        # Assign the match to the developer console
        # Console is always active, but its visibility (in-game GUI or external terminal)
        # is set by an option: showConsoleGUI
        Console.Game = Game
        self.Match = Game
        return Game

    def create_custom(self, rules: Ruleset=None) -> Match:
        """
        Creates a custom match with specified rules.
        """

        if rules == None:
            rules = Ruleset()

        Gameboard = Board()
        Gameboard.surface = chips_surface
        Gameboard.init()

        Scores = Scoreboard() 
        Scores.surface = game_side_surface
        Scores.init()

        Game = Match()
        Game.Surface = chips_surface
        Game.Board = Gameboard
        Game.Scores = Scores
        Game.Rules = rules  
        Game.init()
        
        Console.Game = Game
        self.Match = Game
        return Game

    def get_rules(self) -> Ruleset:
        """
        Returns the match's ruleset.
        """
        if self.Game != None:
            return self.Game.Rules

    def add_match(self):
        """
        Adds a match to the Main queue and starts it.
        """
        self.Queue.put(self.start_match)

    def create_and_start_match(self, mode):

        self.create_match(mode)
        self.start_match()

    def start_match(self, match: Match=None):
        """
        Starts the actual match.
        """

        if match == None:
            if self.Match != None:
                match = self.Match
            else:
                print("No match created.")
                return

        global thread_running, text_mode, global_timer_text

        if match.Rules.allowActions:
            actions = Actions()
            actions.Surface = screen
            actions.Game = match
            actions.Console = Console
            actions.init()

        if match.Rules.allowCheats:
            cheats = Cheats()
            cheats.Surface = screen
            cheats.Game = match
            cheats.Console = Console
            cheats.init()
        
        # This can be set as soon as the match is created
        if match.Rules.mode == 'Classic':
            turn_timer.set_duration(60)
            global_timer.set_duration(1200)
        elif match.Rules.mode == 'Speed':
            turn_timer.set_duration(15)
            global_timer.set_duration(300)

        # This too
        if versusAI:
            text_mode = font_cookie_run_reg.render(str(match.Rules.mode)+" (vs Xena)", True, OAR_BLUE)
        else:
            text_mode = font_cookie_run_reg.render(str(match.Rules.mode), True, OAR_BLUE)

        TIMERTHREAD = threading.Thread(target=timer_thread, daemon=True)

        if enableDebugMode:
            print(f'[Debug]: Playing on {match.Rules.mode} mode')

        pygame.mixer.music.stop()
        full_trans_reset()

        match.IsRunning = True
        while match.IsRunning:
            if match.Rules.enableTimer:
                if not TIMERTHREAD.is_alive():
                    TIMERTHREAD.start() 

            mins, secs = global_timer.get_remaining_time()
            if global_timer.is_running:
                timer_color = WHITE
            else:
                timer_color = LIGHT_GRAY
            global_timer_text = font_cookie_run_reg.render(str(f'{mins:02d}:{secs:02d}'), True, timer_color)

            # change_volume(SOUND_VOLUME)
            #screen.blit(CLEAR_BG, (0, 0)) 
            screen.fill(OAR_BLUE)    
            screen.blit(side_menu_surface, (0, 0))
            side_menu_surface.fill(DARK_GRAY_BLUE)      
            
            if self.Match.winner() != None:
                print(self.Match.winner()) 
                GameIsRunning = False
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

            # Render coordinates surface
            board_area_surface.blit(board_x_coords_surface, board_x_coords_rect)
            board_area_surface.blit(board_y_coords_surface, board_y_coords_rect)
            board_x_coords_surface.fill(DARK_GRAY_BLUE)
            board_y_coords_surface.fill(DARK_GRAY_BLUE)

            # Renders chips
            board_area_surface.blit(chips_surface, (tiles_rect))
            
            # Render captured pieces
            if not match.Board.IsFlipped:
                board_area_surface.blit(right_captured_pieces_surface, (right_captured_pieces_rect))
                board_area_surface.blit(left_captured_pieces_surface, (left_captured_pieces_rect))
            else:
                board_area_surface.blit(right_captured_pieces_surface, (left_captured_pieces_rect))
                board_area_surface.blit(left_captured_pieces_surface, (right_captured_pieces_rect))
            right_captured_pieces_surface.fill(OAR_BLUE)
            left_captured_pieces_surface.fill(OAR_BLUE)
            
            # Display side bar elements
            mini_title.display()

            match.Board.draw()

            screen.blit(text_scores,
                        (game_side_surface.get_width()//2-text_scores.get_width()//2, game_side_surface.get_height()*0.2))

            screen.blit(global_timer_text,
                        (game_side_surface.get_width()//2-global_timer_text.get_width()//2, game_side_surface.get_height()*0.825)) 

            screen.blit(text_mode,
                        (game_side_surface.get_width()//2-text_mode.get_width()//2, game_side_surface.get_height()*0.9))

            if match.Rules.allowActions:
                actions.draw_menu()

            if match.Rules.allowCheats:
                cheats.draw_menu()

                if cheats.ShowEVWindow:
                    if cheats.ev_window.collidepoint(m_pos):
                        cheats.check_for_hover(m_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameIsRunning = False
                    thread_running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        if match.Rules.allowCheats:
                            if cheats.ShowDropdown:
                                cheats.hide_menus()
                            else:
                                pause(match.Rules.mode)
                        else:
                            pause(match.Rules.mode)
                        break
                # Legacy cheat codes
                    if match.Rules.allowCheats:
                        _keys = pygame.key.get_pressed()
                        
                        if _keys[pygame.K_LCTRL]:

                            if _keys[pygame.K_w]: # king pieces

                                if _keys[pygame.K_1]: # blue pieces
                                    drow, dcol = get_cell_from_mouse(pygame.mouse.get_pos())
                                    piece = match.Board.get_piece((drow, dcol))
                                    if dcol % 2 == 1:
                                        if drow % 2 == 1:
                                            if piece.color == RED:
                                                match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                                match.Board.board[drow][dcol].king = True
                                                match.Board.red_left -= 1
                                                match.Board.white_left += 1
                                            elif piece.color == 0:
                                                match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                                match.Board.board[drow][dcol].king = True
                                                match.Board.white_left += 1                                 
                                    else:
                                        if drow % 2 == 0:
                                            if piece.color == RED:
                                                match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                                match.Board.board[drow][dcol].king = True
                                                match.Board.red_left -= 1
                                                match.Board.white_left += 1
                                            elif piece.color == 0:
                                                match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                                match.Board.board[drow][dcol].king = True
                                                match.Board.white_left += 1  

                                if _keys[pygame.K_2]: # red pieces
                                    drow, dcol = get_cell_from_mouse(pygame.mouse.get_pos())
                                    piece = match.Board.get_piece((drow, dcol))
                                    if dcol % 2 == 1:
                                        if drow % 2 == 1:
                                            if piece.color == LIGHT_BLUE:
                                                match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                                match.Board.board[drow][dcol].king = True
                                                match.Board.red_left += 1
                                                match.Board.white_left -= 1
                                            elif piece.color == 0:
                                                match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                                match.Board.board[drow][dcol].king = True
                                                match.Board.red_left += 1                                 
                                    else:
                                        if drow % 2 == 0:
                                            if piece.color == LIGHT_BLUE:
                                                match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                                match.Board.board[drow][dcol].king = True
                                                match.Board.red_left += 1
                                                match.Board.white_left -= 1
                                            elif piece.color == 0:
                                                match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                                match.Board.board[drow][dcol].king = True
                                                match.Board.red_left += 1  

                            elif _keys[pygame.K_1]: # add normal blue piece
                                drow, dcol = get_cell_from_mouse(pygame.mouse.get_pos())
                                piece = match.Board.get_piece((drow, dcol))
                                if dcol % 2 == 1:
                                    if drow % 2 == 1:
                                        if piece.color == RED:
                                            match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            match.Board.red_left -= 1
                                            match.Board.white_left += 1
                                        elif piece.color == 0:
                                            match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            match.Board.white_left += 1                                 
                                else:
                                    if drow % 2 == 0:
                                        if piece.color == RED:
                                            match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            match.Board.red_left -= 1
                                            match.Board.white_left += 1
                                        elif piece.color == 0:
                                            match.Board.board[drow][dcol] = Piece(drow, dcol, LIGHT_BLUE, 100)
                                            match.Board.white_left += 1  

                            elif _keys[pygame.K_2]: # add normal red piece
                                drow, dcol = get_cell_from_mouse(pygame.mouse.get_pos())
                                piece = match.Board.get_piece((drow, dcol))
                                if dcol % 2 == 1:
                                    if drow % 2 == 1:
                                        if piece.color == LIGHT_BLUE:
                                            match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            match.Board.red_left += 1
                                            match.Board.white_left -= 1
                                        elif piece.color == 0:
                                            match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            match.Board.red_left += 1                                 
                                else:
                                    if drow % 2 == 0:
                                        if piece.color == LIGHT_BLUE:
                                            match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            match.Board.red_left += 1
                                            match.Board.white_left -= 1
                                        elif piece.color == 0:
                                            match.Board.board[drow][dcol] = Piece(drow, dcol, RED, 100)
                                            match.Board.red_left += 1

                        if _keys[pygame.K_LSHIFT]:
                            if _keys[pygame.K_c]: # change turn
                                match.change_turn()
                            if _keys[pygame.K_1]: # match resets
                                match.reset()
                            if _keys[pygame.K_2]: # blue wins
                                match.scoreboard.p1_score = 1
                                match.scoreboard.p2_score = 0
                                match.Board.orange_pieces_count = 0
                            if _keys[pygame.K_3]: # red wins
                                match.scoreboard.p1_score = 0
                                match.scoreboard.p2_score = 1
                                match.Board.blue_pieces_count = 0
                            if _keys[pygame.K_4]: # make all pieces king
                                for i in range(8):
                                    for j in range(8):
                                        match.Board.board[i][j].IsKing = True
                            if _keys[pygame.K_5]: # make all pieces not king
                                for i in range(8):
                                    for j in range(8):
                                        match.Board.board[i][j].IsKing = False   
                            if _keys[pygame.K_6]: # removes all pieces
                                for i in range(8):
                                    for j in range(8):
                                        match.Board.board[i][j] = Piece(chips_surface, i, j, 0, 0)
                            if _keys[pygame.K_7]: # displays a single chip in both ends
                                for i in range(8):
                                    for j in range(8):
                                        match.Board.board[i][j] = Piece(chips_surface, i, j, 0, 0)
                                match.Board.board[0][2] = Piece(chips_surface, 0, 2, PLAYER_TWO, 2)   
                                match.Board.board[7][7] = Piece(chips_surface, 7, 7, PLAYER_ONE, 2)  
                                match.Board.red_left = 1
                                match.Board.white_left = 1
                            if pygame.mouse.get_pressed()[2]: #removes the piece
                                drow, dcol = get_cell_from_mouse(pygame.mouse.get_pos())
                                piece = [match.Board.get_piece((drow, dcol))]
                                match.Board.move_to_graveyard(piece)

                        if _keys[pygame.K_m]:
                            if _keys[pygame.K_0]:
                                match.set_mode('Naturals')
                            elif _keys[pygame.K_1]:
                                match.set_mode('Integers')
                            elif _keys[pygame.K_2]:
                                match.set_mode('Rationals')
                            elif _keys[pygame.K_3]:
                                match.set_mode('Radicals')
                            elif _keys[pygame.K_4]:
                                match.set_mode('Polynomials')
                    
                        if cheats.IsTyping:
                            if event.key == pygame.K_RETURN:
                                print(cheats.input)
                                cheats.input.text = ''
                            elif event.key == pygame.K_BACKSPACE:
                                cheats.input.text = cheats.input.text[:-1]
                            else:
                                cheats.input.text += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Left click
                    if pygame.mouse.get_pressed()[0]:
                        
                        if board_rect.collidepoint(m_pos):
                            cell = get_cell_from_mouse_raw(m_pos)
                            col, row = cell

                            if match.moved_piece != None:
                                if row != match.moved_piece.row or row != match.moved_piece.col:
                                    INVALID_SOUND.play()
                                
                            if match.Rules.allowCheats:
                                if not cheats.ShowDropdown:
                                    if (-1 < row < ROWS) and (-1 < col < COLS):
                                        if match.IsMultiplayer:
                                            Console.listen(match.select(cell))
                                        if versusAI:
                                            if match.turn == PLAYER_ONE:
                                                match.select(cell)
                                        else:
                                            match.select(cell)
                            else:
                                if (-1 < row < ROWS) and (-1 < col < COLS):
                                    if versusAI:
                                        if match.turn == PLAYER_ONE:
                                            match.select(cell)
                                    else:
                                        match.select(cell)
                                    
                        if match.Rules.allowActions:
                            if actions.ShowDropdown:
                                if actions.dropdown.window.collidepoint(m_pos):
                                    actions.invoke()
                                elif actions.ShowFFWindow or actions.ShowODWindow:
                                    if actions.confirmation_window.collidepoint(m_pos):
                                        x, y = event.pos
                                        # btn_selected(x, y, btn_list=[actions.button_ff_yes, actions.button_no, actions.button_od_yes])
                                    else:
                                        actions.hide_menus()
                                else:
                                    actions.hide_menus()

                        if match.Rules.allowCheats:
                            if cheats.ShowDropdown:
                                if cheats.dropdown.window.collidepoint(m_pos) and not cheats.ShowEVWindow:
                                    cheats.invoke()
                                elif cheats.ShowEVWindow:
                                    if cheats.ev_window.collidepoint(m_pos):
                                        # Clicked on "Done"
                                        if cheats.selected_done == 1:
                                            cheats.invoke()
                                            cheats.hide_menus()
                                        
                                        # Clicked on text box
                                        if cheats.text_box_rect.collidepoint(m_pos):
                                            cheats.IsTyping = True
                                            cheats.input_box.clear()
                                    else:
                                        cheats.hide_menus()
                                else:
                                    cheats.IsTyping = False
                                    cheats.hide_menus()
                                
                    # Right click
                    if pygame.mouse.get_pressed()[2]:
                        if match.Rules.allowCheats:
                            cell = get_cell_from_mouse_raw(m_pos)
                            col, row = cell

                            if not cheats.ShowEVWindow:
                                cheats.select(cell)

                                if (-1 < row < ROWS) and (-1 < col < COLS):
                                    cheats.create_dropdown(m_pos)
                                    actions.hide_menus()
                                else:
                                    if not game_side_surface.get_rect().collidepoint(m_pos):
                                        cheats.create_dropdown(m_pos, OnBoard=False)
                                        actions.hide_menus()
                                    else:
                                        actions.create_dropdown(m_pos)
                                        cheats.hide_menus()

            screen.blit(CURSOR, pygame.mouse.get_pos())
            match.update()
            pygame.display.update()
            clock.tick(FPS)

# Start console
Console = DeveloperConsole()

Main = Damath()
Console.Main = Main
Console.start()
Main.create_match("Classic")
Main.start()


# Main.splash()