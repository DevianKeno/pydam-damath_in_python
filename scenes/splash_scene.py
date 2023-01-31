
import pygame
from time import sleep
from ui_class.scene import *
from objects import black_background, splash


class S_Splash(Scene):

    def __init__(self) -> None:
        super().__init__()

    def on_exit(self):
        return super().on_exit()

    def display(self):
        screen.blit(black_background, (0, 0))
        splash.display()


SplashScene = S_Splash()