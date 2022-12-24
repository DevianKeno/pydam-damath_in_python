import pygame
from .constants import *
from objects import square_size
from assets import BLUE_PIECE, ORANGE_PIECE, BLUE_PIECE_KING, ORANGE_PIECE_KING
from ui_class.title import Image

class Piece(Image):

    def __init__(self, surface, row, col, color, number):
        self.surface = surface
        self.row = row
        self.col = col
        self.color = color
        self.number = number
        self.num = None
        self.CanMove = True
        self.HasPossibleCapture = False
        self.IsKing = False
        self.IsOnPromotion = False
        self.HasSkipped = False
        self.x = 0
        self.y = 0
        self.w = square_size * 0.874
        self.h = square_size

        self.font = pygame.font.Font('font\CookieRun_Bold.ttf', 18)
        self.text_surface = self.font.render(str(number), True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))

        if self.color == RED:
            self.image = pygame.transform.smoothscale(ORANGE_PIECE, (self.w, self.h))
            self.image_king = pygame.transform.smoothscale(ORANGE_PIECE_KING, (self.w, self.h))
        else:
            self.image = pygame.transform.smoothscale(BLUE_PIECE, (self.w, self.h))
            self.image_king = pygame.transform.smoothscale(BLUE_PIECE_KING, (self.w, self.h))

        super().__init__(self.image, self.surface, (self.x, self.y), (self.w, self.h))
        self.calc_pos()

    def calc_pos(self):
        self.x = square_size * self.col + square_size//2 - self.w//2
        self.y = square_size * self.row

    def make_king(self):
        self.IsOnPromotion = True
        self.IsKing = True

    def done_promote(self):
        self.IsOnPromotion = False

    def can_capture(self, bool=True):
        self.HasPossibleCapture = bool

    def draw(self, surface, number, color):
        if not self.IsKing:
            surface.blit(self.image, (self.x, self.y))
            return
        else:
            surface.blit(self.image_king, (self.x, self.y))
            
        surface.blit(self.text_surface, self.text_rect) 

    def display(self):
        if not self.IsKing:
            self.surface.blit(self.image, (self.x, self.y))
            return
        else:
            self.surface.blit(self.image_king, (self.x, self.y))
            
        self.surface.blit(self.text_surface, self.text_rect) 


    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)

    def num_equivalent(self):
        return int(self.number)