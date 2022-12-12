import pygame, sys

from damath.constants import BOARD_WIDTH, BOARD_HEIGHT, BLACK, WHITE, SQUARE_SIZE, RED, SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT
from ui_class.constants import START_BTN_DIMENSION, START_BTN_POSITION
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT, LOGO_png
from ui_class.button import Button
from ui_class.fade import *
from damath.game import Game
from damath.scoreboard import Scoreboard

# --------- piece move function ---------
def get_row_col_from_mouse(pos):
    x, y = pos
    row = (y-15) // SQUARE_SIZE
    col = (x-300) // SQUARE_SIZE
    return row, col

# --------- initialization ---------
pygame.init()
pygame.font.init()
pygame.mixer.init()

# --------- defining constants / objects for screen  ---------
reso = pygame.display.Info() # gets the video display information object
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
FPS = 60
BG_COLOR = '#FFE3C3'
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Damath') # window caption
pygame.display.set_icon(LOGO_png)
clock = pygame.time.Clock()

# --------- blitting Start button ---------


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

# --------- instantiating the Damath Board and Scoreboard  ---------
board_surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT)) # creating a Surface object where the board will be placed
board_rect = pygame.Rect(300, 15, BOARD_WIDTH, BOARD_HEIGHT) #creating a Rect object to save the position & size of the board
#board_surface.fill(WHITE)
scoreboard_surface = pygame.Surface((SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT))
scoreboard_rect = pygame.Rect(45, 125, SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)
scoreboard = Scoreboard(scoreboard_surface)

game = Game(board_surface, scoreboard)
# --------- instantiating Pause objects ---------
paused_rect = pygame.Rect((SCREEN_WIDTH//2-175, SCREEN_HEIGHT//2-200, 350, 400))
paused_surface = pygame.Surface((paused_rect.w, paused_rect.h))
paused_surface.set_colorkey((0, 0, 0))

# pause menu options
resume_btn = Button(paused_surface, 250, 50, (paused_rect.w//2-125, 60), 5, None, text='Resume', fontsize=24)
restart_btn = Button(paused_surface, 250, 50, (paused_rect.w//2-125, 135), 5, None, text='Restart', fontsize=24)
pause_options_btn = Button(paused_surface, 250, 50, (paused_rect.w//2-125, 210), 5, None, text='Options', fontsize=24)
quit_btn = Button(paused_surface, 250, 50, (paused_rect.w//2-125, 285), 5, None, text='Quit Game', fontsize=24)
# --------- main function ---------
# (Main Menu)
def main_menu() :
    while True:
        screen.fill(BG_COLOR) # window color
        #screen.blit(LOGO_png, (SCREEN_WIDTH//2-(LOGO_png.get_width()//2), SCREEN_HEIGHT//2-(LOGO_png.get_height()//2)-100))
        current_mouse_x, current_mouse_y = pygame.mouse.get_pos() # gets the curent mouse position
        # button hover effect
        # if the cursor is inside the button
        if start_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            option_btn.reset() 
            start_btn.hover_update(start_game)
        elif option_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            start_btn.reset()
            option_btn.hover_update(options_menu)
        else:
            start_btn.reset()
            option_btn.reset() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   

        start_btn.draw()
        option_btn.display_image()
        pygame.display.update()
        clock.tick(FPS)

# --------- pause function ---------
def pause():

    board_surface.set_alpha(50)
    scoreboard_surface.set_alpha(50)   
    screen.blit(scoreboard_surface, (scoreboard_rect.x, scoreboard_rect.y))
    screen.blit(board_surface, (board_rect.x, board_rect.y))

    paused = True

    while paused:   

        screen.blit(paused_surface, (paused_rect.x, paused_rect.y))
    
        current_mouse_x, current_mouse_y = pygame.mouse.get_pos() # gets the curent mouse position
        #print(current_mouse_x, current_mouse_y)
      
        if resume_btn.top_rect.collidepoint((current_mouse_x-paused_rect.x, current_mouse_y-paused_rect.y)):
            resume_btn.hover_update(start_game, delay=1)
            restart_btn.reset()
            pause_options_btn.reset()
            quit_btn.reset()
        elif restart_btn.top_rect.collidepoint((current_mouse_x-paused_rect.x, current_mouse_y-paused_rect.y)):
            restart_btn.hover_update(game.reset)
            resume_btn.reset()
            pause_options_btn.reset()
            quit_btn.reset()
        elif pause_options_btn.top_rect.collidepoint((current_mouse_x-paused_rect.x, current_mouse_y-paused_rect.y)):
            pause_options_btn.hover_update(options_menu)
            resume_btn.reset()
            restart_btn.reset()
            quit_btn.reset()
        elif quit_btn.top_rect.collidepoint((current_mouse_x-paused_rect.x, current_mouse_y-paused_rect.y)):
            resume_btn.reset()
            restart_btn.reset()
            pause_options_btn.reset()   
            quit_btn.hover_update(main_menu, game.reset(), delay=1)   
        else:
            quit_btn.reset()
            resume_btn.reset()
            restart_btn.reset()
            pause_options_btn.reset()           

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    paused = not paused   

        pygame.draw.rect(paused_surface, '#493407', (0, 0, paused_rect.w, paused_rect.h), border_radius=25)
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

        if game.winner() != None:
            print(game.winner()) 
            running = False      

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

        board_surface.set_alpha()
        scoreboard_surface.set_alpha()                          
        screen.blit(scoreboard_surface, (scoreboard_rect.x, scoreboard_rect.y))
        screen.blit(board_surface, (board_rect.x, board_rect.y))   
        scoreboard.draw()
        return_btn.display_image()      

        game.update()
        clock.tick(60)
 
# --------- options menu function ---------
# (when options button is pressed)
def options_menu():
    print("Options Button: Clicked")
    running = True
    screen.fill(BG_COLOR)
    while running:

        current_mouse_x, current_mouse_y = pygame.mouse.get_pos() # gets the curent mouse position
        if return_btn.top_rect.collidepoint((current_mouse_x, current_mouse_y)):
            return_btn.hover_update(main_menu)
        else:
            return_btn.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fade(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                    running = False
                    pygame.display.update()

        return_btn.display_image()                     
        pygame.display.update()
        clock.tick(60)

main_menu()