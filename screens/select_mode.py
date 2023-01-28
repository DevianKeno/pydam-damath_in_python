import pygame
from .main_menu_screen import MainMenu
from ui_class.colors import *
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from objects import sidebar, btn_size, classic_btn, speed_btn, custom_btn, \
        start_select_btn, modes_btn, modes_btn_group, title, TITLE
from ui_class.mode_window import ModeWindow
from .window_functions import custom_window

class SelectMode(MainMenu):

    def __init__(self, bg_color, bg_music=None):
        super().__init__(bg_color, bg_music)

        self.text = 'Modes'
        self.window_function = custom_window

        self.mode_window = ModeWindow(self.screen, (sidebar.sidebar_rect.x+
                            (0.0075*sidebar.sidebar_rect.w), SCREEN_HEIGHT*0.5),
                            200, 300, '#486582', border_color='#425D78', 
                            border_radius=10, border_thickness=8, button_pos=(0, 0),
                            button_width=125, button_height=50, button_text=" ",
                            button_shadow_offset=8)

    @property
    def btn_position(self) -> tuple:
        """
        updates the button's position every frame, 
        this is necessary if its position is affected by moving surfaces 
        (e.g. sidebar expanding / collapsing)
        as this makes the button's position responsive and not fixed
        """
        return [(sidebar.sidebar_rect.width + self.main_screen/10, title.y+TITLE.get_height()*1.5),
                       (((sidebar.sidebar_rect.width + self.main_screen/10 + btn_size[0])+(sidebar.sidebar_rect.width + 
                            self.main_screen - self.main_screen/10 - btn_size[0]))/2 - btn_size[0]/2, title.y+TITLE.get_height()*1.5),
                       ((sidebar.sidebar_rect.width + self.main_screen - self.main_screen/10 - btn_size[0]), title.y+TITLE.get_height()*1.5)], \
                       ((sidebar.sidebar_rect.width + self.main_screen - self.main_screen/10 - btn_size[0]), SCREEN_HEIGHT*0.85)

    @property
    def window_size(self) -> dict:
        """
        Returns an updated window size
        """
        return {
                'x': sidebar.sidebar_rect.w+(0.05*SCREEN_WIDTH), 
                'y' : title.y+TITLE.get_height()*2.2, 
                'width' : SCREEN_WIDTH-(0.05*SCREEN_WIDTH)- (sidebar.sidebar_rect.w+(0.05*SCREEN_WIDTH)),
                'height' : SCREEN_HEIGHT*0.75-(title.y+TITLE.get_height()*2.25)
            }

    def _draw_buttons(self):
        '''
        Buttons layer
        '''
        modes_btn_group.draw(self.btn_position[0], caller_new_pos=self.btn_position[1])

    def _draw_tooltip(self):
        '''
        Tooltip layer
        '''
        for btn in modes_btn:
            if btn.btn_rect.collidepoint((pygame.mouse.get_pos())):
                btn.show_tooltip(1)
                
    def before_looping(self):

        self.initialize()
        classic_btn.set_args('Classic')
        speed_btn.set_args('Speed')
        custom_btn.set_args(None)
        start_select_btn.set_state(start_select_btn.Disabled)

        for btn in modes_btn:
            btn.set_state(btn.Normal)  

    def while_looping(self):
        if self.fade_screen.finished:
            self.display_mode_name()
            self.mode_window.rect_window.wupdate(**self.window_size)
            self.mode_window.draw()
            self._draw_buttons()

        if self.title_moved:
            self.title_slide_above_screen()
            self.mode_window.rect_window.wupdate(**self.window_size)
            self.call_target(self.window_function)
        else:
            self.reset_title_position()
            self.mode_window.rect_window.wupdate(**self.window_size)

        self.display_sidebar('sb_play')
        self.display_logo()
        self.title_slide_up(self.fade_screen)
        self._draw_tooltip()

    def after_looping(self):
        pass
    
select_mode_screen = SelectMode(OAR_BLUE)