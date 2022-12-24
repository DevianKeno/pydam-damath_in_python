import pygame
from .constants import *
from assets import BLUE_PIECE, ORANGE_PIECE, BLUE_PIECE_KING, ORANGE_PIECE_KING
from objects import chips_surface

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

        self.calc_pos()

        if self.color == RED:
            self.image = ORANGE_PIECE
            self.image_king = ORANGE_PIECE_KING
        else:
            self.image = BLUE_PIECE
            self.image_king = BLUE_PIECE_KING

        # self.image_size = (chips_surface.get_width()/8, chips_surface.get_height()/8)
        self.w = 50
        self.h = 50

        # pygame.transform.smoothscale(self.image, self.image_size)
        # pygame.transform.smoothscale(self.image_king, self.image_size)
        pygame.transform.smoothscale(self.image, (self.w, self.h))
        pygame.transform.smoothscale(self.image_king, (self.w, self.h))

    def calc_pos(self):
        self.x = SQUARE_SIZE *  self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.IsOnPromotion = True
        self.IsKing = True

    def done_promote(self):
        self.IsOnPromotion = False

    def can_capture(self, bool=True):
        self.HasPossibleCapture = bool

    def draw(self, surface, number, color):

        font = pygame.font.Font('font\CookieRun_Bold.ttf', 18) #18 = fontsize
        text_surface = font.render(str(number), True, BLACK) #FFFFFF
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        
        if not self.IsKing:
            surface.blit(self.image, (self.x, self.y))
            return
        else:
            surface.blit(self.image_king, (self.x, self.y))

        surface.blit(text_surface, text_rect)
        
        # PIECE_SIZE = (62, 62)
        # if color == RED:
        #     if self.IsKing:
        #         surface.blit(pygame.transform.smoothscale(ORANGE_PIECE_KING, PIECE_SIZE), (self.x-(PIECE_SIZE[0]/2), self.y-(PIECE_SIZE[0]/2)))
        #     else:
        #         surface.blit(pygame.transform.smoothscale(ORANGE_PIECE, PIECE_SIZE), (self.x-(PIECE_SIZE[0]/2), self.y-(PIECE_SIZE[0]/2)))
        # else:
        #     if self.IsKing:
        #         surface.blit(pygame.transform.smoothscale(BLUE_PIECE_KING, PIECE_SIZE), (self.x-(PIECE_SIZE[0]/2), self.y-(PIECE_SIZE[0]/2)))   
        #     else:
        #         surface.blit(pygame.transform.smoothscale(BLUE_PIECE, PIECE_SIZE), (self.x-(PIECE_SIZE[0]/2), self.y-(PIECE_SIZE[0]/2)))           
        

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)

    def num_equivalent(self):
        return int(self.number)