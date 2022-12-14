import pygame, sys, random

from damath.constants import BOARD_WIDTH, BOARD_HEIGHT, BLACK, WHITE, SQUARE_SIZE, RED, LIGHT_BLUE, \
SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT, SCOREBOARD_COLOR, BOARD_BLACK, OFFSET, BOARD_OFFSET, BOARD_BROWN, BOARD_GREEN, BOARD_LIGHTBROWN, \
BOARD_BROWN_2, BOARD_BROWN_3, BOARD_BLUE, BOARD_PINK, BLUE_PIECE, RED_PIECE, BLUE_PIECE_KING, RED_PIECE_KING
from ui_class.constants import START_BTN_DIMENSION, START_BTN_POSITION
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT, LOGO, TITLE, BG_COLOR
from ui_class.button import Button
from ui_class.fade import *
from damath.piece import Piece
from damath.game import Game
from damath.scoreboard import Scoreboard
from ui_class.themes_option import Themes, ThemesList

# --------- piece move function ---------
def get_row_col_from_mouse(pos):
    x, y = pos
    row = (y-board_rect.y-OFFSET) // SQUARE_SIZE
    col = (x-board_rect.x-OFFSET) // SQUARE_SIZE
    return row, col

def anim_dim():
    return random.randrange(0-CHIP_WIDTH, SCREEN_WIDTH, 1), 0-CHIP_HEIGHT

# --------- initialization ---------
pygame.init()
pygame.font.init()
pygame.mixer.init()

# --------- defining constants / objects for screen  ---------

reso = pygame.display.Info() # gets the video display information object
SCREEN_WIDTH = 1080 #reso.current_w #1080
SCREEN_HEIGHT = 720 #reso.current_h #720
FPS = 60
#BG_COLOR = '#240032'

ANIM_SPEED = 3
ANIM_ALPHA = 180 # opacity (0 - transparent, 255 - opaque)
CHIP_WIDTH = 360
CHIP_HEIGHT = 240

#BG_COLOR = '#FFE3C3'
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('DamPY') # window caption
pygame.display.set_icon(LOGO)
clock = pygame.time.Clock()

# --------- Falling Spinning Chip Animation assets ---------

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
red_chips = []

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
start_btn = Button(screen, START_BTN_DIMENSION[0], START_BTN_DIMENSION[1], START_BTN_POSITION, 4, None, text='Start') # w, h, (x, y), radius, image=None, text

# --------- instantiating Options button ---------
option_img_filepath = 'img\\settings-25-512.png'
option_img = pygame.transform.smoothscale(pygame.image.load(option_img_filepath), (36, 36)).convert_alpha()
option_btn = Button(screen, 80, 65, (SCREEN_WIDTH/2+150, (SCREEN_HEIGHT/4)*3), 4, image=option_img, image_size=(36, 36)) # w, h, (x, y), radius, image, text=None

# --------- instantiating the Return button ---------
return_img_filepath = 'img\\button-return.png'
RETURN_DIMENSION = (30, 30)
return_img = pygame.transform.smoothscale(pygame.image.load(return_img_filepath), (RETURN_DIMENSION)).convert_alpha()
return_btn = Button(screen, 70, 70, (20, 20), 4, image=return_img, image_size=RETURN_DIMENSION) # w, h, (x, y), radius, image, text=None

# --------- list of available themes in the game ---------
themes = ThemesList(screen)

BOARDS = [BOARD_BLACK, BOARD_GREEN, BOARD_BROWN, BOARD_LIGHTBROWN,
          BOARD_PINK, BOARD_BROWN_2, BOARD_BROWN_3, BOARD_BLUE]

for idx, board in enumerate(BOARDS):
    themes.append(Themes(screen, board, idx))

BOARD_DEFAULT_THEME = themes.list[themes.focused].board #black board

# --------- instantiating the Damath Board and Scoreboard  ---------
board_surface = pygame.Surface((BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET)) # creating a Surface object where the board will be placed
board_rect = pygame.Rect(375, 25, BOARD_WIDTH+BOARD_OFFSET, BOARD_HEIGHT+BOARD_OFFSET) #creating a Rect object to save the position & size of the board

scoreboard_surface = pygame.Surface((SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT))
scoreboard_rect = pygame.Rect(45, 125, SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)
scoreboard = Scoreboard(scoreboard_surface)

big_blue_chip = SpinningChip(screen, 'blue')
big_red_chip = SpinningChip(screen, 'red')

game = Game(board_surface, scoreboard, BOARD_DEFAULT_THEME)  
# --------- instantiating Pause objects ---------
paused_rect = pygame.Rect((SCREEN_WIDTH//2, SCREEN_HEIGHT//2-200, 350, 400))
paused_surface = pygame.Surface((paused_rect.w, paused_rect.h), pygame.SRCALPHA)
#paused_surface.set_colorkey((0, 0, 0))

# pause menu options
pause_return_btn = Button(screen, 70, 70, (20, 20), 4, image=return_img, image_size=RETURN_DIMENSION) # w, h, (x, y), radius, image, text=None

resume_btn = Button(screen, 250, 50, (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//1.5-265), 5, None, text='Resume', fontsize=24)
restart_btn = Button(screen, 250, 50, (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//1.5-190), 5, None, text='Restart', fontsize=24)
pause_options_btn = Button(screen, 250, 50, (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//1.5-115), 5, None, text='Options', fontsize=24)
quit_btn = Button(screen, 250, 50, (SCREEN_WIDTH//1.5, SCREEN_HEIGHT//1.5-40), 5, None, text='Quit Game', fontsize=24)

# --------- instantiating Options objects ---------


# sliders
music_slider = pygame.transform.smoothscale(BLUE_PIECE_KING, (50, 50))



# --------- main function ---------
# (Main Menu)
def main_menu() :

    game.reset()

    while True:
        #screen.fill(BG_COLOR) # window color
        screen.fill(BG_COLOR)

        for i in range(len(red_chips)):
            red_chips[i].next_frame()
            blue_chips[i].next_frame()

        current_mouse_x, current_mouse_y = pygame.mouse.get_pos() # gets the curent mouse position
        # button hover effect
        # if the cursor is inside the button
        if start_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            option_btn.reset() 
            start_btn.hover_update(start_game)
        elif option_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            start_btn.reset()
            option_btn.hover_update(options_menu, param='main')
        else:
            start_btn.reset()
            option_btn.reset() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
                
        start_btn.draw()
        option_btn.display_image()
        screen.blit(TITLE, (SCREEN_WIDTH//2-(TITLE.get_width()//2), SCREEN_HEIGHT//2-(TITLE.get_height()//(1.25))))
        pygame.display.update()
        clock.tick(FPS)

# --------- pause function ---------

def pause():
    paused = True

    while paused:
        screen.fill(BG_COLOR)

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

        current_mouse_x, current_mouse_y = pygame.mouse.get_pos() # gets the curent mouse position
        #print(current_mouse_x, current_mouse_y)
      
        if resume_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            resume_btn.hover_update(start_game, delay=1)
            restart_btn.reset()
            pause_options_btn.reset()
            quit_btn.reset()
        elif restart_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            restart_btn.hover_update(game.reset)
            if pygame.mouse.get_pressed()[0]:
                start_game()
            pause_options_btn.reset()
            quit_btn.reset()
        elif pause_options_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            pause_options_btn.hover_update(options_menu, param='pause')
            resume_btn.reset()
            restart_btn.reset()
            quit_btn.reset()
        elif quit_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            resume_btn.reset()
            restart_btn.reset()
            pause_options_btn.reset()   
            quit_btn.hover_update(main_menu, delay=1)   
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
        pygame.display.update()
        clock.tick(60)

# --------- start game function ---------
# (when Start button is pressed)
def start_game():

    running = True
    
    while running:
        screen.fill(BG_COLOR)
        
        screen.blit(board_surface, (board_rect.x, board_rect.y))     
        screen.blit(scoreboard_surface, (scoreboard_rect.x, scoreboard_rect.y)) 

        if game.winner() != None:
            print(game.winner()) 
            running = False
            main_menu()   

        current_mouse_x, current_mouse_y = pygame.mouse.get_pos() # gets the curent mouse position
        if return_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            return_btn.hover_update(pause, _fade=False)
        else:
            return_btn.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    pause()
                    break
            # test codes
                _keys = pygame.key.get_pressed()

                if _keys[pygame.K_LSHIFT]:
                    if _keys[pygame.K_c]: # change turn
                        game.change_turn()
                    if _keys[pygame.K_1]: # game resets
                        game.reset()
                    if _keys[pygame.K_2]: # blue wins
                        game.scoreboard.player1_score = 1
                        game.scoreboard.player2_score = 0
                        game.board.red_left = 0
                    if _keys[pygame.K_3]: # red wins
                        game.scoreboard.player1_score = 0
                        game.scoreboard.player2_score = 1
                        game.board.red_left = 0
                    if _keys[pygame.K_4]: # make all pieces king
                        for i in range(8):
                            for j in range(8):
                                game.board.board[i][j].king = True
                    if _keys[pygame.K_5]: # make all pieces not king
                        for i in range(8):
                            for j in range(8):
                                game.board.board[i][j].king = False   
                    if _keys[pygame.K_6]: # removes all pieces
                        for i in range(8):
                            for j in range(8):
                                game.board.board[i][j] = Piece(i, j, 0, 0)
                    if _keys[pygame.K_7]: # displays a single chip in both ends
                        for i in range(8):
                            for j in range(8):
                                game.board.board[i][j] = Piece(i, j, 0, 0)
                        game.board.board[0][1] = Piece(0, 1, LIGHT_BLUE, 2)   
                        game.board.board[7][6] = Piece(7, 6, RED, 2)  
                        game.board.red_left = 1
                        game.board.white_left = 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if board_rect.collidepoint((current_mouse_x, current_mouse_y)):
                        """
                        gets the x and y position of the mouse,
                        and get its corresponding position in the board
                        """
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        game.select(row, col)

        scoreboard.draw()
        return_btn.display_image()     
        game.board.update_theme(themes.list[themes.focused].board)
        game.update()
        clock.tick(60)
 
# --------- options menu function ---------
# (when options button is pressed)
def options_menu(who_called_me):
    
    print("Options Button: Clicked")

    running = True

    while running:

        screen.fill(BG_COLOR)

        for idx, theme in enumerate(themes.list):
            themes.rect_list[idx] = pygame.Rect(theme.x, theme.y, theme.theme.get_width(), theme.theme.get_height())

        for i in range(3):
            red_chips[i].next_frame()
            blue_chips[i].next_frame()
        
        current_mouse_x, current_mouse_y = pygame.mouse.get_pos() # gets the curent mouse position

        themes.display()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                    running = False
                    pygame.display.update()
                
                if event.key == pygame.K_LEFT:
                    themes.move('right')

                if event.key == pygame.K_RIGHT:
                    themes.move('left')

                if event.key == pygame.K_RETURN:
                    game.board.update_theme(themes.list[themes.focused].board)
                    if 'main' is who_called_me:
                        main_menu()
                    elif 'pause' is who_called_me:
                        pause()                    

        if return_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            if 'main' is who_called_me:
                return_btn.hover_update(main_menu)
            elif 'pause' is who_called_me:
                return_btn.hover_update(start_game)
        elif themes.rect_list[themes.focused].collidepoint((current_mouse_x, current_mouse_y)):
            return_btn.reset()
            if pygame.mouse.get_pressed()[0]:
                game.board.update_theme(themes.list[themes.focused].board)
                if 'main' is who_called_me:
                    main_menu()
                elif 'pause' is who_called_me:
                    pause()
        else:
            return_btn.reset()

        return_btn.display_image()        
        pygame.display.update()
        clock.tick(60)

main_menu()