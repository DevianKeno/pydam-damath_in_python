import pygame
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from .main_menu_screen import MainMenuScreen
from objects import modes_btn_group, modes_btn, classic_btn, speed_btn, custom_btn, start_select_btn, \
            TITLE, sidebar, title, btn_size
from ui_class.colors import *
from ui_class.mode_window import ModeWindow
from .sidebar_display import custom_window

class SelectModeScreen(MainMenuScreen):

    def __init__(self, screen: pygame.Surface, bg_color, bg_music=None, on_loop: bool = True, target=None):
        super().__init__(screen, bg_color, bg_music, on_loop, target)

        self.text = 'Modes'
        self.window_function = custom_window

        self.mode_window = ModeWindow(screen, (sidebar.sidebar_rect.x+
                            (0.0075*sidebar.sidebar_rect.w), SCREEN_HEIGHT*0.5),
                            200, 300, '#486582', border_color='#425D78', 
                            border_radius=10, border_thickness=8, button_pos=(0, 0),
                            button_width=125, button_height=50, button_text=" ",
                            button_shadow_offset=8)

        # self.event_list = None

    def before_looping(self):

        classic_btn.set_args('Classic')
        speed_btn.set_args('Speed')
        custom_btn.set_args(None)
        start_select_btn.set_state(start_select_btn.Disabled)

        for btn in modes_btn:
            btn.set_state(btn.Normal)    

        super().before_looping()

    def while_looping(self):
    
        self.screen.fill(self.bg_color)    

        if self.fade_screen.finished:

            # updates the button's position every frame, 
            # this is necessary if its position is affected by moving surfaces 
            # (e.g. sidebar expanding / collapsing)
            # as this makes the button's position responsive and not fixed
            btn_pos = [(sidebar.sidebar_rect.width + self.main_screen/10, title.y+TITLE.get_height()*1.5),
                       (((sidebar.sidebar_rect.width + self.main_screen/10 + btn_size[0])+(sidebar.sidebar_rect.width + 
                            self.main_screen - self.main_screen/10 - btn_size[0]))/2 - btn_size[0]/2, title.y+TITLE.get_height()*1.5),
                       ((sidebar.sidebar_rect.width + self.main_screen - self.main_screen/10 - btn_size[0]), title.y+TITLE.get_height()*1.5)]        

            self.mode_window.rect_window.wupdate(x=sidebar.sidebar_rect.w+(0.05*SCREEN_WIDTH),
                        y=title.y+TITLE.get_height()*2.2, width=SCREEN_WIDTH-(0.05*SCREEN_WIDTH)-
                        (sidebar.sidebar_rect.w+(0.05*SCREEN_WIDTH)),
                        height=SCREEN_HEIGHT*0.75-(title.y+TITLE.get_height()*2.25))
            
            self.mode_window.draw()

            modes_btn_group.draw(btn_pos, caller_new_pos=((sidebar.sidebar_rect.width + 
                        self.main_screen - self.main_screen/10 - btn_size[0]), SCREEN_HEIGHT*0.85))

        super().while_looping()

