import pygame
from .constants import *
from objects import square_size, p1_captured_pieces_surface, p2_captured_pieces_surface
from assets import BLUE_PIECE, ORANGE_PIECE, BLUE_PIECE_KING, ORANGE_PIECE_KING
from ui_class.image import Image

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
        self.IsCaptured = False
        self.x = 0
        self.y = 0
        self.w = square_size * 0.874
        self.h = square_size
        self.font = pygame.font.Font('font\CookieRun_Bold.ttf', int(square_size*0.3))

        if self.color == PLAYER_ONE:
            self.text_surface = self.font.render(str(number), True, DARK_BLUE)
            self.image = pygame.transform.smoothscale(BLUE_PIECE, (self.w, self.h))
            self.image_king = pygame.transform.smoothscale(BLUE_PIECE_KING, (self.w, self.h))
        else:
            self.text_surface = self.font.render(str(number), True, DARK_ORANGE)
            self.image = pygame.transform.smoothscale(ORANGE_PIECE, (self.w, self.h))
            self.image_king = pygame.transform.smoothscale(ORANGE_PIECE_KING, (self.w, self.h))

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

    def display(self):
        if self.IsCaptured:
            if self.color == PLAYER_ONE:
                if self.IsKing:
                    p2_captured_pieces_surface.blit(self.image_king, (self.x, self.y))
                    self.text_surface = self.font.render(str(self.number), True, IMAGINARY_WHITE)
                else:
                    p2_captured_pieces_surface.blit(self.image, (self.x, self.y))
            else:
                if self.IsKing:
                    p1_captured_pieces_surface.blit(self.image_king, (self.x, self.y))
                    self.text_surface = self.font.render(str(self.number), True, IMAGINARY_WHITE)
                else:
                    p1_captured_pieces_surface.blit(self.image, (self.x, self.y))
            self.text_rect = self.text_surface.get_rect(center=(self.x+self.w*0.5, self.y+self.h*0.42))
            self.surface.blit(self.text_surface, self.text_rect)
        else:
            if not self.IsKing:
                self.surface.blit(self.image, (self.x, self.y))
                if self.color == PLAYER_ONE:
                    self.text_surface = self.font.render(str(self.number), True, DARK_BLUE)
                else:
                    self.text_surface = self.font.render(str(self.number), True, DARK_ORANGE)
            else:
                self.surface.blit(self.image_king, (self.x, self.y))
                self.text_surface = self.font.render(str(self.number), True, IMAGINARY_WHITE)
            self.text_rect = self.text_surface.get_rect(center=(self.x+self.w*0.5, self.y+self.h*0.42))
            self.surface.blit(self.text_surface, self.text_rect) 


    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)

    def num_equivalent(self):
        return int(self.number)