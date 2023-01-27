import pygame
from display_constants import SCREEN_WIDTH, SCREEN_HEIGHT, SIDE_MENU_RECT_ACTIVE
from objects import sidebar, anim_title_down, anim_title_upper, sound_slider, music_slider
from .main_menu_screen import MainMenuScreen
from audio_constants import SOUNDS
from ui_class.colors import WHITE

class OptionsMenuScreen(MainMenuScreen):

    def __init__(self, screen: pygame.Surface, bg_color, bg_music=None, on_loop: bool = True, target=None):
        super().__init__(screen, bg_color, bg_music, on_loop, target)

        self.text = 'Options'
        self.options_font = pygame.font.Font('font\CookieRun_Regular.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.06))

    def while_looping(self):

        self.screen.fill(self.bg_color)
        mx, my = pygame.mouse.get_pos()

        if self.fade_screen.finished and anim_title_down.IsFinished:
            # self.screen.blit(self.font.render('Options', True, WHITE), 
            #             (sidebar.sidebar_rect.width + 
            #             (SCREEN_WIDTH-sidebar.sidebar_rect.width)/11, 
            #             SCREEN_HEIGHT/2.5))
            music_slider.draw(int(sidebar.sidebar_rect.width + 
                            (SCREEN_WIDTH-sidebar.sidebar_rect.width)/2.5))
            sound_slider.draw(int(sidebar.sidebar_rect.width + 
                            (SCREEN_WIDTH-sidebar.sidebar_rect.width)/2.5))
            self.screen.blit(self.options_font.render('Music', True, WHITE), 
                        (int(sidebar.sidebar_rect.width + 
                        (SCREEN_WIDTH-sidebar.sidebar_rect.width)/4.65),
                        int(SCREEN_HEIGHT/1.75 - music_slider.height*6)))
            self.screen.blit(self.options_font.render('SFX', True, WHITE), 
                        (int(sidebar.sidebar_rect.width + 
                        (SCREEN_WIDTH-sidebar.sidebar_rect.width)/4.65), 
                        int(SCREEN_HEIGHT/1.50 - music_slider.height*6)))

            if not sound_slider.get_slider_state() and music_slider.get_collider().collidepoint((mx, my)):
                music_slider.update(mx)
                MUSIC_VOLUME = music_slider.get_value()/100
                pygame.mixer.music.set_volume(MUSIC_VOLUME)

            elif not music_slider.get_slider_state() and sound_slider.get_collider().collidepoint((mx, my)):
                sound_slider.update(mx)
                SOUND_VOLUME = sound_slider.get_value()/100
                self.change_volume(SOUND_VOLUME)  

        if anim_title_upper.IsFinished:
            anim_title_down.play()

        return super().while_looping()

    def change_volume(self, vol):
        for sound in SOUNDS:
            sound.set_volume(vol)

