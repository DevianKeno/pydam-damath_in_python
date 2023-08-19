
import sys
import pygame
from ui_class.scene import *
from screens.select_mode import *
from objects import *


class S_Pause(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.name = "Pause Scene"
        self.description = """Game paused."""
        # Scene objects
        self.IsPaused = False
        self.Main = None

    def on_entry(self):
        self.IsPaused = True
        resume_btn.set_target(self.unload())
        options_btn.set_target()
        restart_btn.set_target(None)
        main_menu_btn.set_target(self.unload)

    def display(self):
        global thread_running, paused

        turn_timer.pause()
        global_timer.pause()

        # a function to break the while loop since
        # "break" isn't a function in itself, and 
        # calling the previous caller function 
        # will reset the game / requires more modification
        # to create the desired behavior


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

    def late_update(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

PauseScene = S_Pause()