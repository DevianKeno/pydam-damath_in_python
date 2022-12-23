import pygame
from .constants import RED, WHITE, BLACK, SQUARE_SIZE, CROWN, BLUE_PIECE, RED_PIECE, BLUE_PIECE_KING, RED_PIECE_KING, OFFSET

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
        self.CanMove = True
        self.HasPossibleCapture = False
        self.IsKing = False
        self.IsOnPromotion = False
        self.HasSkipped = False
        self.x = 0
        self.y = 0
        self.calc_pos()

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
        radius = SQUARE_SIZE//2 - self.PADDING
        #pygame.draw.circle(surface, BLACK, (self.x, self.y), radius+ self.OUTLINE)
        #pygame.draw.circle(surface, self.color, (self.x, self.y), radius)

        font = pygame.font.Font('font\CookieRun_Bold.ttf', 18) #18 = fontsize
        text_surface = font.render(str(number), True, BLACK) #FFFFFF
        text_rect = text_surface.get_rect(center=(self.x, self.y))

        PIECE_SIZE = (62, 62)
        if color == RED:
            if self.IsKing:
                surface.blit(pygame.transform.smoothscale(RED_PIECE_KING, PIECE_SIZE), (self.x-(PIECE_SIZE[0]/2), self.y-(PIECE_SIZE[0]/2)))
            else:
                surface.blit(pygame.transform.smoothscale(RED_PIECE, PIECE_SIZE), (self.x-(PIECE_SIZE[0]/2), self.y-(PIECE_SIZE[0]/2)))
        else:
            if self.IsKing:
                surface.blit(pygame.transform.smoothscale(BLUE_PIECE_KING, PIECE_SIZE), (self.x-(PIECE_SIZE[0]/2), self.y-(PIECE_SIZE[0]/2)))   
            else:
                surface.blit(pygame.transform.smoothscale(BLUE_PIECE, PIECE_SIZE), (self.x-(PIECE_SIZE[0]/2), self.y-(PIECE_SIZE[0]/2)))           
        
        surface.blit(text_surface, text_rect)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)

    def num_equivalent(self):
        return int(self.number)