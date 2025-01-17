# 
# Damath
# 
from __future__ import annotations
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
from damath.ruleset import *
from damath.scoreboard import Scoreboard
from damath.constants import *
from damath.timer import *
from display_constants import *
from event_loop import event_loop
from screens.select_mode import select_mode_screen
from screens.options_menu import options_screen
from screens.multi_menu import MultiMenu
from ui_class.button import Button, ButtonList
from ui_class.colors import * 
from ui_class.constants import START_BTN_DIMENSION, START_BTN_POSITION
from ui_class.fade import *
from ui_class.main_menu import *
from ui_class.themes_option import Themes, ThemesList
from ui_class.image import *
from ui_class.scene import *
from ui_class.tween import *
from ui_class.rect_window import *
from ui_class.mode_window import *
from queue import Queue
# Multiplayer
from audio_constants import * 
from objects import *
from assets import *
from options import *

from scenes.title_scene import *
from scenes.game_scene import *
from scenes.host_game_scene import *
from scenes.splash_scene import *

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

    if Options.enableDebugMode:
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

    if col < 0 or col > 7:
        return -1, -1
    if row < 0 or row > 7:
        return -1, -1

    if Options.enableDebugMode:
        print(f"[Debug/Action]: Clicked on cell ({col}, {row}), raw")
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

# --------- Sidebar Targets ---------

def sidebar_init():
    """
    Sets args and target for sidebar options
    """
    for option in list(sidebar.args.keys()):
        if option != 'sb_exit':
            target = display_screen
        else:
            target = sys.exit
        sidebar.get_option(option).target = target
    sidebar.set_args([[select_mode_screen], [multi_mode_screen], [None], [options_screen], [None]])

def sidebar_update(func):
    """
    made update() as a decorator
    """
    def update(Screen):
        sidebar_init()
        return func(Screen)
    return update

# --------- MAIN MENU SCREENS ---------

@sidebar_update
def display_screen(screen):
    if screen == select_mode_screen:
        classic_btn.set_target(Main.create_match)
        classic_btn.set_args("classic")
        speed_btn.set_target(Main.create_match)
        speed_btn.set_args("speed")
        start_select_btn.set_target(Main.start_match)
    
    try:
        screen.display()
    except Exception as e:
        print(e)
# --------- Screen Objects ---------
multi_mode_screen = MultiMenu(OAR_BLUE)

sidebar_init()

# --------- pause function ---------

def pause(mode):
    pass

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
    print(game.check_for_winner() == RED)

    if game.check_for_winner() == PLAYER_TWO:
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


def load():
    SplashScene.load()
    pass

splash_thread = Thread(target=load)


class Damath:

    def __init__(self) -> None:
        self.Queue = Queue()
        self.Match = None
        
    def start(self):
        TitleScene = S_Title()
        TitleScene.Main = self
        TitleScene.load()

    """
    Methods
    """
    def create_match(self, mode: str='classic') -> Match:
        """
        Creates a new self.Match with specified mode.
        The created match is stored as the member "Damath.Match" and is overridden by succeeding created matches.
        """        
        Rules.set_mode(mode)
        self.Match = Match()

    def create_custom(self, rules: Ruleset=None):
        """
        Creates a custom match with specified rules.
        Not passing a Ruleset will set the mode to 'Classic'.
        """
        if rules != None:
            Rules = rules
        else:
            rules = Ruleset()

    def _create_custom_from_rulestr(self, rulestr: str):
        """
        Creates a custom match with the specified rulestring.
        Not passing a rulestring will set the mode to 'Classic'.
        """
        if rules != None:
            Rules.set_rulestr(rulestr)
        else:
            rules = Ruleset()

    def host_match(self, match: Match=None):
        """
        Hosts a multiplayer match.
        """
        if match == None:
            if self.Match != None:
                match = self.Match
            else:
                print("Create a match first.")
                return
        Rules.IsMultiplayer = True

    def set_rules(self, ruleset: Ruleset):
        """
        Set match rules manually.
        """
        if self.Match != None:
            self.Match.Rules = ruleset
        else:
            print("No match to set ruleset to.")

    def get_rules(self) -> Ruleset:
        """
        Returns the match's ruleset.
        """
        if self.Match != None:
            return self.Match.Rules

    def add_match(self):
        """
        Adds a match to the Main queue and starts it.
        """
        self.Queue.put(self.start_match)

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
        
        self.Match.IsRunning = True

        # Initializations
        Gameboard = Board()
        Gameboard.Symbols = Symbol()
        Gameboard.surface = chips_surface
        Gameboard.Symbols.surface = chips_surface
        Gameboard.init()

        Scores = Scoreboard()
        Scores.surface = game_side_surface
        Scores.init()

        self.Match.Surface = chips_surface
        self.Match.Board = Gameboard
        self.Match.Scores = Scores
        self.Match.init()

        if Rules.enableTimer:
            turn_timer.set_duration(Rules.timer_turn)
            global_timer.set_duration(Rules.timer_global)
            turn_timer.Match = self.Match
            GameScene.TurnTimer = turn_timer
            GameScene.GlobalTimer = global_timer

        if Rules.allowActions:
            actions = Actions()
            actions.Surface = screen
            actions.Game = match
            actions.Console = Console
            actions.init()
            GameScene.Actions = actions

        if Rules.allowCheats:
            cheats = Cheats()
            cheats.Surface = screen
            cheats.Game = match
            cheats.Console = Console
            cheats.init()
            GameScene.Cheats = cheats
            
        Console.Game = self.Match

        pygame.mixer.music.stop()

        if Options.enableDebugMode:
            print(f'[Debug]: Playing on {Rules.mode} mode')

        if Console.IsClient:
            Console._command_flip()
            Console._command_lock()

        if Rules.IsMultiplayer:            
            GameScene.Match = match
            GameScene.Console = Console
            GameScene.load()
            # HostGameScene.Match = match
            # HostGameScene.load()
        else:            
            GameScene.Match = match
            GameScene.Console = Console
            GameScene.load()


# ----- Main program -----
# Start console
Console = DeveloperConsole()

Main = None
if not Main:
    Main = Damath()
else:
    Main = Main

Console.Main = Main
Console.start()
Main.start()
