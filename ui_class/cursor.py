from pygame import mouse
from assets import CURSOR
from display_constants import screen


class CustomCursor:

    def __init__(self) -> None:
        pass

    def draw(self, pos: tuple=()):

        if not pos:
            screen.blit(CURSOR, mouse.get_pos())
            return
        screen.blit(CURSOR, pos)
        return


Cursor = CustomCursor()