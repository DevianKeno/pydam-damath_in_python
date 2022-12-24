import pygame
from .constants import *
from objects import chips_surface
from assets import BLUE_PIECE, ORANGE_PIECE, BLUE_PIECE_KING, ORANGE_PIECE_KING

SQUARE_SIZE = chips_surface.get_width()/8

class Piece:

    def __init__(self, row, col, color, number):
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
        self.w = SQUARE_SIZE * 0.874
        self.h = SQUARE_SIZE

        self.font = pygame.font.Font('font\CookieRun_Bold.ttf', 18) #18 = fontsize
        self.text_surface = self.font.render(str(number), True, BLACK) #FFFFFF
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))

        if self.color == RED:
            self.image = pygame.transform.smoothscale(ORANGE_PIECE, (self.w, self.h))
            self.image_king = pygame.transform.smoothscale(ORANGE_PIECE_KING, (self.w, self.h))
        else:
            self.image = pygame.transform.smoothscale(BLUE_PIECE, (self.w, self.h))
            self.image_king = pygame.transform.smoothscale(BLUE_PIECE_KING, (self.w, self.h))
            
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2 - self.w//2
        self.y = SQUARE_SIZE * self.row

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

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)

    def num_equivalent(self):
        return int(self.number)