import pygame
from display_constants import TITLE

class Title:

    def __init__ (self, surface, pos):
        """
        Title object.
        """
        self.surface = surface
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    def display(self):
        self.surface.blit(TITLE.convert_alpha(), (self.x, self.y))
        
    # self.speed = 0.25
    # self.start = SCREEN_HEIGHT//2-(TITLE.get_height()//2)
    # self.pos = SCREEN_HEIGHT//2-(TITLE.get_height()//2)
    # self.finished = False #finished reaching height
    # self.reversed = False #reversed after reaching height

    # # nn
    # def play(self):
    #     if not self.reversed:
    #         if self.pos == self.height + self.start:
    #             self.reversed = True
    #             self.pos -= self.speed
    #         elif self.pos == self.height + self.start - 12 or self.pos == self.height + self.start - 4:
    #             self.pos += 2
    #         else:
    #             self.pos += self.speed
    #         self.surface.blit(self.img, ((SCREEN_WIDTH*0.71)//2+(SCREEN_WIDTH*0.29)-(TITLE.get_width()//2), self.pos))
    #     if self.reversed:
    #         if self.pos == self.start - self.height:
    #             self.reversed = False
    #             self.pos += self.speed
    #         elif self.pos == self.start - self.height + 12 or self.pos == self.height + self.start + 4:
    #             self.pos -= 2
    #         else:
    #             self.pos -= self.speed
    #         self.surface.blit(self.img, ((SCREEN_WIDTH*0.71)//2+(SCREEN_WIDTH*0.29)-(TITLE.get_width()//2), self.pos))