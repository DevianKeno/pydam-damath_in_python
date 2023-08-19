import pygame
from .constants import *
from .ruleset import Rules
from objects import square_size, right_captured_pieces_surface, left_captured_pieces_surface
from assets import BLUE_PIECE, ORANGE_PIECE, BLUE_PIECE_KING, ORANGE_PIECE_KING
from ui_class.image import Image
from options import *

class Piece(Image):

    def __init__(self, surface, cell=(), color=None, value=''):
        self.surface = surface
        self.cell = cell
        self.col = cell[0]
        self.row = cell[1]
        self.x = 0
        self.y = 0
        self.w = square_size * 0.874
        self.h = square_size

        self.color = color
        self.number = value
        self.num = None

        self.IsMovable = True
        self.HasSkipped = False
        self.HasPossibleCapture = False
        self.IsCaptured = False
        self.IsKing = False
        self.IsOnPromotion = False
        
        self.font = pygame.font.Font('font\CookieRun_Bold.ttf', int(square_size*0.3))
        
        match Rules.piece_values:
            case 'Rationals':
                self.font = pygame.font.Font('font\CookieRun_Bold.ttf', int(square_size*0.24))
            case 'Radicals':
                self.font = pygame.font.Font('font\CookieRun_Regular.ttf', int(square_size*0.15))
            case 'Polynomials':
                self.font = pygame.font.Font('font\CookieRun_Bold.ttf', int(square_size*0.21))

        if self.color == PLAYER_ONE:
            self.image = pygame.transform.smoothscale(BLUE_PIECE, (self.w, self.h))
            self.image_king = pygame.transform.smoothscale(BLUE_PIECE_KING, (self.w, self.h))
        else:
            self.image = pygame.transform.smoothscale(ORANGE_PIECE, (self.w, self.h))
            self.image_king = pygame.transform.smoothscale(ORANGE_PIECE_KING, (self.w, self.h))

        super().__init__(self.image, self.surface, (self.x, self.y), (self.w, self.h))
        self.calc_pos()

    def calc_pos(self):
        self.x = square_size * self.col + square_size//2 - self.w//2
        self.y = square_size * abs(self.row-7)

    def make_king(self):
        self.IsOnPromotion = True
        self.IsKing = True

    def promote(self):
        self.IsKing = True

    def demote(self):
        self.IsKing = False

    def done_promote(self):
        self.IsOnPromotion = False

    def set_capture_status(self, bool=True):
        self.HasPossibleCapture = bool

    def display(self):
        if self.IsCaptured:
            if self.color == PLAYER_ONE:
                self.text_surface = self.font.render(str(self.number), True, DARK_BLUE)

                if self.IsKing:
                    left_captured_pieces_surface.blit(self.image_king, (self.x, self.y))
                    self.text_surface = self.font.render(str(self.number), True, IMAGINARY_WHITE)
                else:
                    left_captured_pieces_surface.blit(self.image, (self.x, self.y))
            else:
                self.text_surface = self.font.render(str(self.number), True, DARK_ORANGE)
                if self.IsKing:
                    right_captured_pieces_surface.blit(self.image_king, (self.x, self.y))
                    self.text_surface = self.font.render(str(self.number), True, IMAGINARY_WHITE)
                else:
                    right_captured_pieces_surface.blit(self.image, (self.x, self.y))

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

    def move(self, col, row):
        self.col = col
        self.row = row
        self.calc_pos()

    def __repr__(self):
        return str(self.color)

    def num_equivalent(self):
        return int(self.number)