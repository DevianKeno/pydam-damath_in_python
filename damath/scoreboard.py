from .constants import LIGHT_BLUE, RED, WHITE, BLACK, DARKER_BLUE, DARKER_RED, SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT, SCOREBOARD_COLOR, SCOREBOARD_ALPHA
from assets import SCOREBOARD_BLUE, SCOREBOARD_RED, SCOREBOARD_BLUE_ACTIVE, SCOREBOARD_RED_ACTIVE
import pygame, operator
from ui_class.fade import fade
from display_constants import SIDE_MENU_COLOR, BG_COLOR

class Scoreboard:

    TXT_OFFSET = 10

    def __init__(self, surface):
        self.width = SCOREBOARD_WIDTH   
        self.height = SCOREBOARD_HEIGHT
        self.surface = surface

        self.player1_score = 0 #red
        self.player2_score = 0 #blue

        self.font = pygame.font.Font('font\CookieRun_Bold.ttf', 54)

    def draw(self):
        
        self.surface.fill(SIDE_MENU_COLOR)
        pygame.draw.rect(self.surface, BG_COLOR, (0, 18, self.width, self.height//2-35), border_radius=8)
        pygame.draw.rect(self.surface, BG_COLOR, (0, SCOREBOARD_HEIGHT//2+18, self.width, self.height//2-36), border_radius=8)

    def update(self, turn):

        blue_box = pygame.Rect((0, 18, self.width, self.height//2-35)) 
        red_box = pygame.Rect((0, SCOREBOARD_HEIGHT//2+18, self.width, self.height//2-36))

        if turn == RED: 

            p1_score_surface = self.font.render(str(round(self.player1_score, 1)), True, SIDE_MENU_COLOR) #FFFFFF
            p1_score_rect = p1_score_surface.get_rect(center=blue_box.center)
            self.surface.blit(p1_score_surface, p1_score_rect) 

            p2_score_surface = self.font.render(str(round(self.player2_score, 1)), True, SIDE_MENU_COLOR) #FFFFFF
            p2_score_rect = p2_score_surface.get_rect(center=red_box.center)
            self.surface.blit(p2_score_surface, p2_score_rect)

        else:

            p2_score_surface = self.font.render(str(round(self.player2_score, 1)), True, SIDE_MENU_COLOR) #FFFFFF
            p2_score_rect = p2_score_surface.get_rect(center=red_box.center)
            self.surface.blit(p2_score_surface, p2_score_rect)

            p1_score_surface = self.font.render(str(round(self.player1_score, 1)), True, SIDE_MENU_COLOR) #FFFFFF
            p1_score_rect = p1_score_surface.get_rect(center=blue_box.center)
            self.surface.blit(p1_score_surface, p1_score_rect) 
        

    def score_update(self, color, piece, numbers, operations):
        result = 0
        OPERATOR_MAP = {'+' : operator.add,
                        '-' : operator.sub,
                        'x' : operator.mul,
                        '÷' : operator.truediv}
        print(numbers)
        for num, operation in zip(numbers, operations):
            op = OPERATOR_MAP.get(operation)
            if operation == '÷' and num.number == 0:
                continue
            else:
                result += op(piece.number, num.number)
                if piece.IsKing:
                    if piece.IsOnPromotion:
                        piece.done_promote()
                    else:
                        result *= 2.
                    
                    
            print("+", result)

        if color == RED:
            self.player1_score += result
        else:
            self.player2_score += result

        print(f'Player 1: {self.player1_score}\n' \
                f'Player 2: {self.player2_score}')       

    def score(self):
        return self.player1_score, self.player2_score

    def reset(self):
        self.player1_score = 0 #red
        self.player2_score = 0 #blue