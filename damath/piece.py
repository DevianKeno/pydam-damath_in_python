import pygame
from .constants import RED, WHITE, BLACK, SQUARE_SIZE, CROWN, BLUE_PIECE, RED_PIECE, BLUE_PIECE_KING, RED_PIECE_KING

class Piece:

    #class variable
    PADDING = 12
    OUTLINE = 2
    
    def __init__(self, row, col, color, number):
        self.row = row
        self.col = col
        self.color = color
        self.number = number
        self.num = None
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE *  self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, surface, number, color):
        radius = SQUARE_SIZE//2 - self.PADDING
        #pygame.draw.circle(surface, BLACK, (self.x, self.y), radius+ self.OUTLINE)
        #pygame.draw.circle(surface, self.color, (self.x, self.y), radius)

        font = pygame.font.Font("font/GlacialIndifference-Bold.ttf", 24) #18 = fontsize
        text_surface = font.render(str(number), True, BLACK) #FFFFFF
        text_rect = text_surface.get_rect(center=(self.x, self.y))

        if color == RED:
            if self.king:
                surface.blit(pygame.transform.smoothscale(RED_PIECE_KING, (66, 66)), (self.x-33, self.y-33))
            else:
                surface.blit(pygame.transform.smoothscale(RED_PIECE, (66, 66)), (self.x-33, self.y-33))
        else:
            if self.king:
                surface.blit(pygame.transform.smoothscale(BLUE_PIECE_KING, (66, 66)), (self.x-33, self.y-33))   
            else:
                surface.blit(pygame.transform.smoothscale(BLUE_PIECE, (66, 66)), (self.x-33, self.y-33))           
        
        surface.blit(text_surface, text_rect)

        """if self.king:
            surface.blit(CROWN, (self.x - CROWN.get_width()//2, self.y-radius))"""

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)

    def num_equivalent(self):
        return int(self.number)