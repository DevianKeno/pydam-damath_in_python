
from ui_class.scene import *
from screens.select_mode import *
from objects import *
from damath.ruleset import *
from damath.piece import *
from console import *
from audio_constants import *


class S_HostGame(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.name = "Host Game Scene"
        self.description = """Scene where host waits for an opponent."""
        # Scene objects
        self.Console = None
        self.Match = None

    def on_entry(self):
        self.text_mode = font_cookie_run_reg.render("-", True, OAR_BLUE)
        timer_color = OAR_BLUE
        self.GlobalTimer_text = font_cookie_run_reg.render('--:--', True, timer_color)

    def display(self):
        screen.fill(OAR_BLUE)    
        screen.blit(side_menu_surface, (0, 0))
        side_menu_surface.fill(DARK_GRAY_BLUE)
        screen.blit(game_side_surface, (0, 0))
        game_side_surface.fill(DARK_GRAY_BLUE)
        screen.blit(board_area_surface, (game_side_surface.get_width(), 0))
        board_area_surface.fill(OAR_BLUE)

        damath_board.display()

        self.Match.Board.set_surface_alpha()

        # Renders chips
        board_area_surface.blit(chips_surface, (tiles_rect))
        
        # Display side bar elements
        mini_title.display()

        screen.blit(text_scores,
                    (game_side_surface.get_width()//2-text_scores.get_width()//2, game_side_surface.get_height()*0.2))
        screen.blit(self.GlobalTimer_text,
                    (game_side_surface.get_width()//2-self.GlobalTimer_text.get_width()//2, game_side_surface.get_height()*0.825)) 
        screen.blit(self.text_mode,
                    (game_side_surface.get_width()//2-self.text_mode.get_width()//2, game_side_surface.get_height()*0.9))
  
        self.Match.Scores.draw_scores()

HostGameScene = S_HostGame()