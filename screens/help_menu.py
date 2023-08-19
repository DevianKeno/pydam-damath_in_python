import pygame
from pygame import gfxdraw
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from objects import sidebar, anim_title_down, anim_title_upper
from .main_menu_screen import MainMenuScreen
from ui_class.rect_window import create_window
from ui_class.new_btn import NButton

class HelpMenuScreen(MainMenuScreen):

    def __init__(self, screen: pygame.Surface, bg_color, bg_music=None, on_loop: bool = True, target=None):
        super().__init__(screen, bg_color, bg_music, on_loop, target)

        self.text = 'Help'

    def before_looping(self):

        self.t1_rectwin = create_window(self.screen, (sidebar.sidebar_rect.x+
                    (0.0075*sidebar.sidebar_rect.w), SCREEN_HEIGHT*0.5), 
                    200, 300, '#486582', border_color='#425D78', 
                    border_radius=10, border_thickness=8, cast_shadow=False)

        self.expand_btn = NButton(self.screen, (0, 0), 125, 50, border_radius=8, shadow_offset=8)
        
        super().before_looping()

    def while_looping(self):

        self.screen.fill(self.bg_color)

        if anim_title_down.IsFinished and self.fade_screen.finished:
            self.t1_rectwin.wupdate(x=sidebar.sidebar_rect.w+(0.25*sidebar.sidebar_rect.w),
                                width=SCREEN_WIDTH-(0.25*sidebar.sidebar_rect.w)-
                                (sidebar.sidebar_rect.w+(0.25*sidebar.sidebar_rect.w)),
                                height=SCREEN_HEIGHT*0.125)

            self.t1_rectwin.draw()

            self.expand_btn.draw((self.t1_rectwin.x+self.t1_rectwin.w*0.5-self.expand_btn.get_rect().w*0.5, 
                            self.t1_rectwin.y+self.t1_rectwin.h-
                            self.expand_btn.get_rect().h*0.5))

            gfxdraw.filled_polygon(self.screen, 
                                [
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.4), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.25)), 
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.6), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.25)),
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.625), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.3)),
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.515), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.75)),
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.485), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.75)),
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.375), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.3))
                                ],
                                pygame.Color('#486582'))

            gfxdraw.aapolygon(self.screen, 
                                [
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.4), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.25)), 
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.6), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.25)),
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.625), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.3)),
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.525), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.75)),
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.475), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.75)),
                                (int(self.expand_btn.get_rect().x+self.expand_btn.get_rect().width*0.375), 
                                int(self.expand_btn.get_rect().y+self.expand_btn.get_rect().height*0.3))
                                ],
                                pygame.Color('#425D78'))

        if anim_title_upper.IsFinished:
            anim_title_down.play()

        super().while_looping()