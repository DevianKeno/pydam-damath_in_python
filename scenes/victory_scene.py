
from ui_class.scene import *
from ui_class.text import *
from objects import *
from ui_class.tween import *

class S_Win(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.name = "Victory Scene"
        self.description = """A player has won."""
        # Scene objects
        self.Match = None
        ## Text elements
        self.victory_message = None
        self.win_condition = None
        self.anim_window_pop_up = None

    def on_entry(self):
        victory_window.wupdate(x = (SCREEN_WIDTH * 0.5) - (victory_window.width * 0.5), 
                               y = (SCREEN_HEIGHT * 0.5) - (victory_window.h * 0.5))
                
        self.victory_message = Text(screen, CookieRun_Regular, victory_window.h * 0.1, WHITE)
        self.win_condition = Text(screen, CookieRun_Regular, victory_window.h * 0.05, OAR_BLUE)

        self.victory_message.text = "Victory!"
        self.victory_message.pos = ((victory_window.x + victory_window.w // 2),
                                (victory_window.y + victory_window.h * 0.2))

        self.win_condition.text = "Captured all opponents pieces"
        self.win_condition.pos = ((victory_window.x + victory_window.w // 2),
                                (victory_window.y + victory_window.h * 0.3))

    def display(self):
        victory_window.draw()

        self.victory_message.draw()
        self.win_condition.draw()


VictoryScene = S_Win() 