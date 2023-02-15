
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
        resume_btn.set_target(self.unload())
        # options_btn.set_target()
        # restart_btn.set_target(None)
        # main_menu_btn.set_target(self.unload)

    def display(self):
        screen.blit(alpha_surface, (0, 0))
        alpha_surface.set_alpha(125)

        # displays the pause window elements
        pause_window.wupdate(x=SCREEN_WIDTH*0.5-pause_window.width*0.5, 
                        y=SCREEN_HEIGHT*0.5-pause_window.h*0.5)
        pause_window.draw()

        screen.blit(pause_text, (pause_window.x+(pause_window.w*0.5-
                            pause_text.get_width()*0.5), 
                            SCREEN_HEIGHT*0.25))
        
        pause_buttons_group.draw()

        # the attribute pos_reset is checked to see
        # if the NButton object has been previously clicked 
        # and is now no longer clicked, which means the function
        # is already called and the pause window should now close
        # (used to prevent executing the function without the button 
        # behaving in its selected state first once clicked)
        # if resume_btn.pos_reset:
        #     turn_timer.resume()
        #     global_timer.resume()

        # if restart_btn.pos_reset:
        #     start_game(mode)

PauseScene = S_Pause() 