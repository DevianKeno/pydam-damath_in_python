import pygame
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from .main_menu_screen import MainMenu, anim_title_slide_down, anim_title_slide_past_screen
from objects import TITLE, sidebar, title, \
        multi_local_btn, multi_online_btn, multi_button_group, \
        multi_join_btn, btn_size, ICON_BUFFERING
from ui_class.mode_window import ModeWindow
from ui_class.colors import OAR_BLUE
class MultiMenu(MainMenu):

    rot_idx = 360
    buffering_icon = pygame.transform.smoothscale(ICON_BUFFERING, (int(multi_join_btn.height*2), int(multi_join_btn.height*2)))   
    
    def __init__(self, bg_color, bg_music=None):
        super().__init__(bg_color, bg_music)

        self.text = 'Multi'

        self.mode_window = ModeWindow(self.screen, (sidebar.sidebar_rect.x+
                            (0.0075*sidebar.sidebar_rect.w), SCREEN_HEIGHT*0.5),
                            200, 300, '#486582', border_color='#425D78', 
                            border_radius=10, border_thickness=8, button_pos=(0, 0),
                            button_width=125, button_height=50, button_text=" ",
                            button_shadow_offset=8)

    @property
    def btn_pos(self) -> list:
        return [((sidebar.sidebar_rect.w+(self.main_screen*0.5))-
                        multi_local_btn.btn_rect.w*1.1, title.y+TITLE.get_height()*1.5),
                        ((sidebar.sidebar_rect.w+(self.main_screen*0.5))+
                        multi_online_btn.btn_rect.w*0.1, title.y+TITLE.get_height()*1.5)]

    @property
    def window_size(self) -> dict:
        return {
                'x' : sidebar.sidebar_rect.w+(0.05*SCREEN_WIDTH), 
                'y' : title.y+TITLE.get_height()*2.2,
                'width' : SCREEN_WIDTH-(0.05*SCREEN_WIDTH)- (sidebar.sidebar_rect.w+(0.05*SCREEN_WIDTH)), 
                'height' : SCREEN_HEIGHT*0.75-(title.y+TITLE.get_height()*2.25)
            }

    def multi_window(self):

        multi_join_btn.draw(((sidebar.sidebar_rect.width + 
                (SCREEN_WIDTH-sidebar.sidebar_rect.width) - 
                (SCREEN_WIDTH-sidebar.sidebar_rect.width)/10 - 
                btn_size[0]), 
                SCREEN_HEIGHT*0.85))
        
        window_text = pygame.font.Font('font/CookieRun_Regular.ttf', int(multi_join_btn.height*0.6))
        window_text_surface = window_text.render("Searching for available matches...", True, OAR_BLUE)
        self.screen.blit(window_text_surface, (self.mode_window.rect_window.x + self.mode_window.rect_window.w*0.5 - window_text_surface.get_width()*0.5,
                    self.mode_window.rect_window.y+(self.mode_window.rect_window.h*0.55)))

        #NOTE: a make-do rotate function for now as I can't seem to move the previously instantiated tween object and it only stays in the middle of the screen
        rotated_image = pygame.transform.rotate(self.buffering_icon, self.rot_idx)
        centered = rotated_image.get_rect(center=(self.mode_window.rect_window.x + self.mode_window.rect_window.w*0.5, 
                    self.mode_window.rect_window.y+(self.mode_window.rect_window.h*0.45)))
        self.screen.blit(rotated_image, centered)
        
        if self.rot_idx < 0:
            self.rot_idx = 360
        else:
            self.rot_idx-=4

    def _draw_buttons(self):
        multi_button_group.draw(self.btn_pos)

    def _draw_tooltip(self):
        for btn in [multi_local_btn, multi_online_btn]:
            if btn.btn_rect.collidepoint((pygame.mouse.get_pos())):
                btn.show_tooltip(1)

    def before_looping(self):
        self.initialize()
        multi_local_btn.set_state(multi_local_btn.Normal)

    def while_looping(self):

        if self.fade_screen.finished:
            self.display_mode_name()
            self._draw_buttons()

            if multi_local_btn.toggled:
                self.title_moved = True
            else:
                self.title_moved = False

        if self.title_moved:
            self.title_slide_above_screen()
            self.mode_window.rect_window.wupdate(**self.window_size)
            self.mode_window.draw()
            if anim_title_slide_past_screen.IsFinished:
                self.multi_window()
        else:
            self.reset_title_position()
            self.mode_window.rect_window.wupdate(**self.window_size)
            if anim_title_slide_down.IsPlaying:
                self.mode_window.draw()
            else:
                '''
                #TODO: insert fade animation for mode window here
                '''

        self.display_sidebar('sb_online')
        self.display_logo()
        self.title_slide_up(self.fade_screen)
        self._draw_tooltip()

    def after_looping(self):
        pass
        
        
        