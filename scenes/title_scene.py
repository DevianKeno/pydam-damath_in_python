
import sys
import pygame
from ui_class.scene import *
from screens.select_mode import *
from objects import *

clock = pygame.time.Clock()


class S_Title(Scene):

    def __init__(self) -> None:
        super().__init__()
        self.name = "Title Scene"
        self.description = """Main title screen at the start of the game."""
        # Scene objects
        self.Main = None

    def on_entry(self):
        print(f"{self.name} has been loaded.")

    def on_exit(self):
        print(f"{self.name} has been unloaded.")

    def update(self):
        print(f"I am called every frame.")

    def display(self):
        try:
            _start_match = self.Main.Queue.get(False)
            _start_match()
        except: 
            pass

        screen.fill(OAR_BLUE)
        screen.blit(title_surface, (((SCREEN_WIDTH-sidebar.sidebar_rect.w) // 2) +
                    sidebar.sidebar_rect.w-title_surface.get_width() // 2, 0))
        title_surface.fill(OAR_BLUE)
        sidebar.display(None)
        screen.blit(LOGO, (sidebar.sidebar_rect.width/2 - LOGO.get_width()/2, side_menu_surface.get_height()*0.075))
        title.display()

        anim_title_breathe.play()

    def late_update(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.unload()
                    self.Main.create_match('classic')
                    self.Main.start_match()
                    return

                if event.key == pygame.K_MINUS:
                    self.unload()
                    return
                
                if event.key == pygame.K_t:
                    self.unload()
                    select_mode_screen.display()
                    return

TitleScene = S_Title()