import pygame
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from .main_menu_screen import MainMenuScreen
from objects import TITLE, sidebar, title, multi_local_btn, multi_online_btn, multi_button_group, mode_window
from ui_class.colors import *
from .sidebar_display import multi_window
from ui_class.mode_window import ModeWindow

class MultiMenuScreen(MainMenuScreen):

    def __init__(self, screen: pygame.Surface, bg_color, bg_music=None, on_loop: bool = True, target=None):
        super().__init__(screen, bg_color, bg_music, on_loop, target)

        self.text = 'Multi'
        self.window_function = multi_window

        self.mode_window = ModeWindow(screen, (sidebar.sidebar_rect.x+
                            (0.0075*sidebar.sidebar_rect.w), SCREEN_HEIGHT*0.5),
                            200, 300, '#486582', border_color='#425D78', 
                            border_radius=10, border_thickness=8, button_pos=(0, 0),
                            button_width=125, button_height=50, button_text=" ",
                            button_shadow_offset=8)

    def before_looping(self):

        multi_local_btn.set_state(multi_local_btn.Normal)

        super().before_looping()

    def while_looping(self):
        
        self.screen.fill(self.bg_color)
        
        if self.fade_screen.finished:
            btn_pos = [((sidebar.sidebar_rect.w+(self.main_screen*0.5))-
                        multi_local_btn.btn_rect.w*1.1, title.y+TITLE.get_height()*1.5),
                        ((sidebar.sidebar_rect.w+(self.main_screen*0.5))+
                        multi_online_btn.btn_rect.w*0.1, title.y+TITLE.get_height()*1.5)]
            
            mode_window.rect_window.wupdate(x=sidebar.sidebar_rect.w+
                    (0.05*SCREEN_WIDTH), y=title.y+TITLE.get_height()*2.2,
                    width=SCREEN_WIDTH-(0.05*SCREEN_WIDTH)- (sidebar.sidebar_rect.w+
                    (0.05*SCREEN_WIDTH)), height=SCREEN_HEIGHT*0.75-(title.y+TITLE.get_height()*2.25))

            self.mode_window.draw()
            
            multi_button_group.draw(btn_pos)

            if multi_local_btn.toggled:
                self.move_title = True
            else:
                self.move_title = False

        super().while_looping()
        

        
        
        