from .constants import LIGHT_BLUE, RED, WHITE, BLACK, DARKER_BLUE, DARKER_RED, SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT, SCOREBOARD_COLOR
import pygame, operator
from ui_class.fade import fade

class Scoreboard:
    def __init__(self, surface):
        self.width = SCOREBOARD_WIDTH
        self.height = SCOREBOARD_HEIGHT
        self.surface = surface

        self.player1_score = 0 #red
        self.player2_score = 0 #blue

    def draw(self):
        self.surface.fill(SCOREBOARD_COLOR)
        pygame.draw.rect(self.surface, LIGHT_BLUE, (10, 10, self.width-20, self.height//2-10))
        pygame.draw.rect(self.surface, RED, (10, self.height//2+10, self.width-20, self.height//2-20))

    def update(self, turn):

        font = pygame.font.Font(None, 78) 

        if turn == RED:
            red_box = pygame.draw.rect(self.surface, DARKER_BLUE, (10, 10, self.width-20, self.height//2-10))
            blue_box = pygame.draw.rect(self.surface, RED, (10, self.height//2+10, self.width-20, self.height//2-20))  

            p1_score_surface = font.render(str(round(self.player1_score, 2)), True, WHITE) #FFFFFF
            p1_score_rect = p1_score_surface.get_rect(center=blue_box.center)
            self.surface.blit(p1_score_surface, p1_score_rect) 

            p2_score_surface = font.render(str(round(self.player2_score, 2)), True, BLACK) #FFFFFF
            p2_score_rect = p2_score_surface.get_rect(center=red_box.center)
            self.surface.blit(p2_score_surface, p2_score_rect)
        else:
            blue_box = pygame.draw.rect(self.surface, DARKER_RED, (10, self.height//2+10, self.width-20, self.height//2-20))
            red_box = pygame.draw.rect(self.surface, LIGHT_BLUE, (10, 10, self.width-20, self.height//2-10))    

            p2_score_surface = font.render(str(round(self.player2_score, 2)), True, WHITE) #FFFFFF
            p2_score_rect = p2_score_surface.get_rect(center=red_box.center)
            self.surface.blit(p2_score_surface, p2_score_rect)

            p1_score_surface = font.render(str(round(self.player1_score, 2)), True, BLACK) #FFFFFF
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