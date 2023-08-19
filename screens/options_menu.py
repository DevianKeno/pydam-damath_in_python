import pygame
from display_constants import SCREEN_HEIGHT, SIDE_MENU_RECT_ACTIVE
from objects import sidebar, anim_title_slide_down, anim_title_slide_past_screen, sound_slider, music_slider
from .main_menu_screen import MainMenu
from audio_constants import SOUNDS
from ui_class.colors import WHITE, OAR_BLUE

class OptionsMenu(MainMenu):

    def __init__(self, bg_color, bg_music=None):
        super().__init__(bg_color, bg_music)
        
        self.text = 'Options'
        self.options_font = pygame.font.Font('font\CookieRun_Regular.ttf', int(SIDE_MENU_RECT_ACTIVE.height*0.06))

    @staticmethod
    def change_volume(vol):
        for sound in SOUNDS:
            sound.set_volume(vol)

    def _detect_collision(self):
        if (not sound_slider.get_slider_state() and 
            music_slider.get_collider().collidepoint((self.mx, self.my))):
                music_slider.update(self.mx)
                MUSIC_VOLUME = music_slider.get_value()/100
                pygame.mixer.music.set_volume(MUSIC_VOLUME)

        elif (not music_slider.get_slider_state() and 
                sound_slider.get_collider().collidepoint((self.mx, self.my))):
                sound_slider.update(self.mx)
                SOUND_VOLUME = sound_slider.get_value()/100
                self.change_volume(SOUND_VOLUME)  

    def _display_slider_text(self):
        self.screen.blit(self.options_font.render('Music', True, WHITE), 
                    (int(sidebar.sidebar_rect.width + 
                    self.main_screen/4.65),
                    int(SCREEN_HEIGHT/1.75 - music_slider.height*6)))
        self.screen.blit(self.options_font.render('SFX', True, WHITE), 
                    (int(sidebar.sidebar_rect.width + 
                    self.main_screen/4.65), 
                    int(SCREEN_HEIGHT/1.50 - music_slider.height*6)))

    def _draw_sliders(self):
        music_slider.draw(int(sidebar.sidebar_rect.width + 
                        self.main_screen/2.5))
        sound_slider.draw(int(sidebar.sidebar_rect.width + 
                        self.main_screen/2.5))

    def before_looping(self):
        self.initialize()

    def while_looping(self):
        if self.fade_screen.finished and anim_title_slide_down.IsFinished:
            self.display_mode_name()
            self._draw_sliders()
            self._display_slider_text()
            self._detect_collision()
        self.display_sidebar('sb_options')
        self.display_logo()
        self.title_slide_up(self.fade_screen)
        self.reset_title_position()

options_screen = OptionsMenu(OAR_BLUE)

